# Based on `background_job.py` stub in Blender
# 
# This script is an example of how you can run blender from the command line
# (in background mode with no interface) to automate tasks, in this example it
# creates a text object, camera and light, then renders and/or saves it.
# This example also shows how you can parse command line options to scripts.
#
# Example usage for this test.
#  blender --background --factory-startup --python $HOME/background_job.py -- \
#          --text="Hello World" \
#          --render="/tmp/hello" \
#          --save="/tmp/hello.blend"
#
# Notice:
# '--factory-startup' is used to avoid the user default settings from
#                     interfering with automated scene generation.
#
# '--' causes blender to ignore all following arguments so python can use them.
#
# See blender --help for details.


import bpy
import numpy as np


def add_random_cube_in_volume(vol_side, seed=None):
    # Clear existing objects.
    # bpy.ops.wm.read_factory_settings(use_empty=True)

    # Instantiate scene
    # scene = bpy.context.scene

    ### If I use mesh I need to define the vertices
    # https://blender.stackexchange.com/questions/61879/create-mesh-then-add-vertices-to-it-in-python
    # https://b3d.interplanety.org/en/how-to-create-mesh-through-the-blender-python-api/ 
    # Add a cube
    # cube_mesh = bpy.data.meshes.new('Box')
    # cube_object =  bpy.data.objects.new(cube_mesh.name, cube_mesh)
    # bpy.data.collections["Collection"].objects.link(cube_object) # to add to scene collection: scene.collection.objects
  
    # # Set its x-location randomly (btw 0 and 1)
    # # rng = default_rng() # recommended constructor for the random number class Generator
    # cube_object.location = (0,0,0) #vol_side*rng.random((3,)) - 0.5*vol_side
    #---------

    ### Via operator
    # add a cube primitive and link it to the scene collection
    bpy.ops.mesh.primitive_cube_add() # returns {'FINISHED'} if successful
    cube_object = bpy.context.object

    # set location randomly within predifined volume
    rng = np.random.default_rng(seed) # recommended constructor for the random number class Generator
    cube_object.location = vol_side*rng.random((3,)) - 0.5*vol_side

    ## Update view layer (not sure if needed)
    # bpy.context.view_layer.update()
    

    


def main():
    # import sys       
    # import argparse 

    # # get Python args (passed after "--")
    # argv = sys.argv
    # if "--" not in argv:
    #     argv = []
    # else:
    #     argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # #---------
    # # initialise parser
    # usage_text = (
    #     "Run blender in background mode with this script:"
    #     "  blender --background --python " + __file__ + " -- [python args]"
    # )
    # parser = argparse.ArgumentParser(description=usage_text)

    # # add arguments to parser
    # # Possible types are: string, int, long, choice, float and complex.
    # # parser.add_argument(
    # #     "-t", "--text", dest="text", type=str, required=True,
    # #     help="This text will be used to render an image",
    # # )

    # # parser.add_argument(
    # #     "-s", "--save", dest="save_path", metavar='FILE',
    # #     help="Save the generated file to the specified path",
    # # )
    # # parser.add_argument(
    # #     "-r", "--render", dest="render_path", metavar='FILE',
    # #     help="Render an image to the specified path",
    # # )

    # # build parser object?
    # args = parser.parse_args(argv)

    # #---------
    # # print help if no arguments provided
    # if not argv:
    #     parser.print_help()
    #     return

    # # error if required arguments not provided
    # if not args.text:
    #     print("Error: --text=\"some string\" argument not given, aborting.")
    #     parser.print_help()
    #     return
    # #---------


    # Run the add random cube function
    vol_side = 1
    add_random_cube_in_volume(vol_side) # pass a specific seed for deterministic behaviour

    print("batch job finished, exiting")


if __name__ == "__main__":
    main()
