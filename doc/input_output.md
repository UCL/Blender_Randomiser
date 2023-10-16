## Min-max bounds via input file
[Example input .json file](/input_bounds.json) for setting bounds. Currently can be used for setting camera transforms, materials and geometry min-max boundaries. Could be extended in the future to use parameter names from the [output .json file](/output_randomisations_per_frame1697116725.310647.json).

The input file is read in as a dictionary with the key names following the pattern of "Values" + "material or geometry name" + "socket name":
 - "Values Geometry Nodes.001RandomSize.001"
 - "Values MaterialRandomMetallic"


## Save parameter outputs button

In this panel, you can set how many frames you want to randomise before clicking the Save Parameter Outputs button. This will randomise all the variables that are toggled on for randomisation and then a dictionary of parameter values are saved to an output .json file.

Due to the layout of geometry/materials panels, they are saved as a dictionary within the overall dictionary.
