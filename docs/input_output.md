## Min-max bounds via input file
There is an [example input .json file](/input_bounds.json) which can be used for setting the randomisation bounds. Currently, it can be used for setting camera transforms, materials and geometry min-max boundaries.

The input file is read into the [install_and_enable_addons.py script](/install_and_enable_addons.py) as a dictionary with the key names for the geometry and materials panels following the pattern of "Values" + "material or geometry name" + "socket name":
 - "Values Geometry Nodes.001RandomSize.001"
 - "Values MaterialRandomMetallic"

The node names that appear in the panels for geometry and materials nodes can be randomised and saved as in the output .json file. The names in this output file can then be used to specify the names of the geometry and materials nodes in the input file.

 > [!NOTE]
> The install_and_enable_addons.py script could be extended in the future to use parameter names from the [output .json file](/output_randomisations_per_frame1697116725.310647.json) to specify the key names for geometry, materials and user-defined properties panels.


## Save parameter outputs panel

This panel allows the user to export the randomised values for the selected properties. The user can set the number of frames for which the randomisation will be executed, before clicking the Save Parameter Outputs button. The values of the selected properties are saved as dictionaries to an [output .json file](/output_randomisations_per_frame1697116725.310647.json). The material and geometry properties are grouped as separate dictionaries, which get appended to the dictionary of all the parameters to be saved.
