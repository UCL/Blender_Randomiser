from random import uniform

import bpy
from bpy.app.handlers import persistent

from .. import utils


# -------------------------------
# Operator
# -------------------------------
class AddCustomPropTolist(bpy.types.Operator):
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

    bl_idname = "opr.add_custom_prop_to_list"  # appended to bpy.ops.
    bl_label = "Add custom prop to list"

    bl_options = {"REGISTER", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    #     # check the context here
    #     return context.object is not None

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

        utils.add_custom_prop_to_custom_list(context)

        return {"FINISHED"}


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


class CUSTOM_OT_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {"REGISTER"}

    action_prop = bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("REMOVE", "Remove", ""),
            ("ADD", "Add", ""),
        )
    )
    action: action_prop  # type: ignore

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == "DOWN" and idx < len(scn.custom) - 1:
                scn.custom[idx + 1].name
                scn.custom.move(idx, idx + 1)
                scn.custom_index += 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    scn.custom_index + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "UP" and idx >= 1:
                scn.custom[idx - 1].name
                scn.custom.move(idx, idx - 1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    scn.custom_index + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "REMOVE":
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({"INFO"}, info)

        if self.action == "ADD":
            item = scn.custom.add()
            item.name = "Your Name"
            item.id = len(scn.custom)
            scn.custom_index = len(scn.custom) - 1
            info = '"%s" added to list' % (item.name)
            self.report({"INFO"}, info)
        return {"FINISHED"}


class CUSTOM_OT_printItems(bpy.types.Operator):
    """Print all items and their properties to the console"""

    bl_idname = "custom.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {"REGISTER", "UNDO"}

    reverse_order_prop = bpy.props.BoolProperty(
        default=False, name="Reverse Order"
    )

    reverse_order: reverse_order_prop  # type: ignore

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.custom_index, -1, -1):
                item = scn.custom[i]
                print("Name:", item.name, "-", "ID:", item.id)
        else:
            for item in scn.custom:
                print("Name:", item.name, "-", "ID", item.id)
        return {"FINISHED"}


class CUSTOM_OT_clearList(bpy.types.Operator):
    """Clear all items of the list"""

    bl_idname = "custom.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({"INFO"}, "All items removed")
        else:
            self.report({"INFO"}, "Nothing to remove")
        return {"FINISHED"}


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    ApplyRandomCustom,
    AddCustomPropTolist,
    CUSTOM_OT_actions,
    CUSTOM_OT_printItems,
    CUSTOM_OT_clearList,
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
