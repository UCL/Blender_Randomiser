import bpy
import numpy as np
import pdb


# -------------------------------
## Operators
class ApplyRandomTransform(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Add a random cube within a predefined volume"""

    bl_idname = "opr.apply_random_transform"  # appended to bpy.ops.
    bl_label = "Apply random transform to object"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current context
    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    # ----------------------
    ## Invoke
    # runs before execute, to initialise ....?
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    # -------------------------------
    ### Execute fn
    def execute(self, context):

        loc = context.scene.randomise_camera_props.camera_pos
        rot = context.scene.randomise_camera_props.camera_rot
        randomise_on=True

        randomize_selected(context, loc, rot, randomise_on)

        
        # # for obj in bpy.context.selected_objects:
        # #     rename_object(obj, params)



        # # add a cube primitive and link it to the scene collection        
        # bpy.ops.mesh.primitive_uv_sphere_add()  # returns {'FINISHED'} if successful
        # cube_object = context.object

        # # get inputs
        # # seed: If None, fresh unpredictable entropy will be pulled from the OS
        # scene = context.scene
        # seed = (
        #     scene.random_cube_props.seed
        #     if scene.random_cube_props.seed_toggle
        #     else None
        # )
        # vol_size = scene.random_cube_props.vol_size

        # # set location randomly within predifined volume
        # rng = np.random.default_rng(
        #     seed
        # )  # recommended constructor for the random number class Generator
        # cube_object.location = vol_size * rng.random((3,)) - 0.5 * vol_size

        return {"FINISHED"}


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    ApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("unregistered")