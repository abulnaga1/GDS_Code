This code creates a pulley waveguide coupler gds file.

Pulley waveguides are a method of evanescent coupling to a ring resonator without having to create a straight section (racetrack) in the resonator.

An example of a pulley coupler in the literature can be found at http://dx.doi.org/10.1038/nphoton.2016.64.

The python code utilizes GDSpy to create the structure. A ring is created as defined by its central radius and cross-section width.

A pulley waveguide is then created and is defined by the pulley waveguide cross-section width, the desired coupling length, and the radius of the bend from the horizontal waveguide region to the coupling region. 
This radius dictates the bending loss moving from a straight waveguide to a curved waveguide.
