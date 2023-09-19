import bpy
from bpy.app.handlers import persistent

from ..transform.operators import get_transform_inputs, randomise_selected


# -------------------------------
# Operator
# -------------------------------
class ApplyRandomAll(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise all the panels

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.randomise_all"  # appended to bpy.ops.
    bl_label = "Apply randomisation to all panels"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the randomiser operator

        Randomise all the panels

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        (
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        ) = get_transform_inputs(context)

        randomise_selected(
            context,
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        )

        return {"FINISHED"}


# -------------------------------
class ApplySaveParams(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Save parameter outputs in .json

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.save_param_out"  # appended to bpy.ops.
    bl_label = "Save parameter outputs"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the save param operator

        Save parameter outputs in .json

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        print("hello")

        return {"FINISHED"}


@persistent
def randomise_all_per_frame(dummy):
    bpy.ops.camera.randomise_all("INVOKE_DEFAULT")

    return


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    ApplyRandomAll,
    ApplySaveParams,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(randomise_all_per_frame)

    print("randomise all operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(randomise_all_per_frame)

    print("randomise all unregistered")
