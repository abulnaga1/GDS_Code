
#Title:         pulley_wX_gapY_MM_DD_YYYY.py
#Description:   CAD file for pulley waveguide simulations (import into lumerical fdtd)
#Authors:       Alex Abulnaga
#Date modified: 2020-08-03  
#Notes:         All units in microns

#Import requisite python packages
import gdspy
import numpy
import math

#Create the cells of the cad file
main_cell = gdspy.Cell("pulley_coupler")

#Define the fixed variables of the structure
ring_r = 25;     #The radius of the ring resonator
ring_w = 0.5;    #The width of the ring resonator waveguide
phc_w = 0.4;     #The width of the photonic crystal waveguide

#Dynamic Variables
Lc = [1, 2, 3, 3.2, 3.5, 4, 5]  
gap = 0.025;                     #The desired gap between the ring resonator and the pulley waveguide in the coupling area
bend_radius = 25;               #The radius of the bend after the coupling region

#Define the calculated variables
ring_ir = ring_r - ring_w/2;    #The inner radius of the ring resonator
ring_or = ring_r + ring_w/2;    #The outer radius of the ring resonator
pulley_r = ring_or + gap + phc_w/2;        #The radius of the pulley waveguide in the coupling region
pulley_ir = pulley_r - phc_w/2; #The inner radius of the pulley waveguide
pulley_or = pulley_r + phc_w/2; #The outer radius of the pulley waveguide

#Create the structures
########################################

#Create the ring resonator for reference
ring = gdspy.Round(
            (0, 0),                            #(x,y) origin of the curve
            ring_or,                           #ring outer radius
            inner_radius=ring_ir,              #ring inner radius
            initial_angle=0,                   #Initial angle of the ring
            final_angle=2*numpy.pi,            #Final angle. We define a 360 degree ring 
            tolerance=0.001,                   #Tolerance of the cell
            layer = 0)                         #Place the ring on a different layer so we can easily change thickness in lumerical
main_cell.add(ring)                            #Add the ring to the cell

#Create a set of pulleys with different coupling length so that we can import them all into lumerical in a single file to do a sweep
for i in range(len(Lc)):             #we will sweep over pulley lengths from 1 to 10um
    arc_angle = Lc[i]/pulley_r       #Calculate the arc angle which gives an arc length Lc, units of radians
    
    #Create the pulley waveguide. We will just create half the waveguide, then mirror it about the vertical axis
    pulley = gdspy.Path(phc_w,(0,pulley_r)); #Define the width of the path and the starting co-ordinates

    pulley.arc(pulley_r,                 #Start by defining the coupling portion which is an arc defined by arc_angle and the pulley radius
          numpy.pi/2,                    #initial angle
          numpy.pi/2 + arc_angle/2,      #final angle
          layer=i+1,                     #Define the layer to match the coupling length
          tolerance = 0.001)             #Curve tolerance 

    pulley.turn(bend_radius,             #We add a turn with radius 15um
            -arc_angle/2,                #We turn the pulley back to parallel with the horizontal axis
            layer = i+1,                 #Layer number matches coupling length. This will help us in lumerical
            tolerance = 0.001)           #Bend tolerance

    pulley.segment(ring_r + pulley.x,        #We add a horizontal section up to a total length of ring_r, so that the horizontal portion extends arbitrarily long
               '-x',                         #We will later only consider a subsection in the FDTD simulation
               layer = i+1)                  #Layer number

    pulley2 = gdspy.copy(pulley)             #Make a copy of the path
    pulley2.mirror((0,0),(0,1))              #And mirror it so we complete the pulley

    main_cell.add(pulley)                    #Add the pulley coupler to the pulley cell
    main_cell.add(pulley2)                   #Add the mirror as well 

gdspy.write_gds('pulley_w400nm_25nmGap_LcSweep_2020_07_08.gds') #Write the GDS file
