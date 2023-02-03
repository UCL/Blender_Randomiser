# Add-on metadata
bl_info = {
    "name": "add random cube in cubic volume centred around the origin",
    "blender": (3,4,1), # get from running bpy.app.version
    "category": "Object",
}

import bpy
import numpy as np


class AddRandomCube(bpy.types.Operator):
    """Add a random cube within a predefined volume"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.add_random_cube"        # this is appended to bpy.ops.
    bl_label = "Add random cube in volume"         # Display name in the interface (this is how it shows in operator search)
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context: 'Context'):
        
        seed = None
        vol_side = 1

        # add a cube primitive and link it to the scene collection
        bpy.ops.mesh.primitive_cube_add() # returns {'FINISHED'} if successful
        cube_object = bpy.context.object

        # set location randomly within predifined volume
        rng = np.random.default_rng(seed) # recommended constructor for the random number class Generator
        cube_object.location = vol_side*rng.random((3,)) - 0.5*vol_side

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddRandomCube.bl_idname)

def register():
    '''This is run when the add-on is enabled'''
    bpy.utils.register_class(AddRandomCube)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    '''This is run when the add-on is disabled'''
    bpy.utils.unregister_class(AddRandomCube)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()