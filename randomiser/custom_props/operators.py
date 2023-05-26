from random import uniform

import bpy
from bpy.app.handlers import persistent


# -------------------------------
# Operator
# -------------------------------
class ApplyRandomCustom(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise the position and orientation of the camera

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "opr.apply_random_custom_prop"  # appended to bpy.ops.
    bl_label = "Apply random to custom prop"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the randomiser operator

        Randomise the position and rotation x,y,z components
        of the camera between their min and max values.

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        cust_min = context.scene.custom_props.custom_min[0]
        cust_max = context.scene.custom_props.custom_max[0]
        cust_range = [cust_min, cust_max]

        rand_cust = context.scene.custom_props.bool_rand_cust

        custom_input = context.scene.custom_props.custom_input
        custom_idx = context.scene.custom_props.custom_idx

        randomise_selected(
            context,
            cust_range,
            rand_cust,
            custom_input,
            custom_idx,
        )

        return {"FINISHED"}

    # def invoke(self, context, event):
    #     return context.window_manager.invoke_props_dialog(self)


@persistent
def randomise_custom_per_frame(dummy):
    bpy.ops.opr.apply_random_custom_prop("INVOKE_DEFAULT")

    return


# --------------------------------------------------
# Randomise_selected function:


def randomise_selected(
    context, cust_range, rand_cust, custom_input, custom_idx
):
    """Generate random numbers between the range for x/y/z
    directions in location and rotation

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    if rand_cust:
        custom_input.split(".")
        # attr_string = list_string[len(list_string)-1]
        # obj_string = custom_input.rsplit(".",1)[0]

        getattr(context.active_object, custom_input)[custom_idx] = uniform(
            cust_range[0], cust_range[1]
        )

    else:  # otherwise the values change under us
        uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    ApplyRandomCustom,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(randomise_custom_per_frame)

    print("transform operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(randomise_custom_per_frame)

    print("transform operators unregistered")
