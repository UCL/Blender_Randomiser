import bpy


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
                scn.custom += 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    scn.custom + 1,
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
            for i in range(scn.custom, -1, -1):
                item = scn.custom[i]
                print("Name:", item.name, "-", "ID:", item.user_defined)
        else:
            for item in scn.custom:
                print("Name:", item.name, "-", "ID", item.user_defined)
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


# -------------------------------
# Operator
# -------------------------------
# class AddUserDefined(bpy.types.Operator):
#     # docstring shows as a tooltip for menu items and buttons.
#     """Randomise the position and orientation of the camera

#     Parameters
#     ----------
#     bpy : _type_
#         _description_

#     Returns
#     -------
#     _type_
#         _description_
#     """

#     bl_idname = "opr.add_user_defined_prop"  # appended to bpy.ops.
#     bl_label = "Add user defined property to panel"

#     bl_options = {"REGISTER", "UNDO"}

#     @classmethod
#     def poll(cls, context):
#         # check the context here
#         return context.object is not None

#     def execute(self, context):
#         """Execute the randomiser operator

#         Randomise the position and rotation x,y,z components
#         of the camera between their min and max values.

#         Parameters
#         ----------
#         context : _type_
#             _description_

#         Returns
#         -------
#         _type_
#             _description_
#         """
#         try:
#             context.scene.user_defined[self.user_defined].select_set(True)
#             return {'FINISHED'}
#         except:
#             print('Could not select object')
#             return {'CANCELLED'}


#         # randomise_selected(
#         #     context,
#         #     loc,
#         #     loc_x_range,
#         #     loc_y_range,
#         #     loc_z_range,
#         #     rot,
#         #     rot_x_range,
#         #     rot_y_range,
#         #     rot_z_range,
#         #     delta_on,
#         #     rand_posx,
#         #     rand_posy,
#         #     rand_posz,
#         #     rand_rotx,
#         #     rand_roty,
#         #     rand_rotz,
#         # )

#         return {"FINISHED"}


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    CUSTOM_OT_actions,
    CUSTOM_OT_printItems,
    CUSTOM_OT_clearList,
]

# AddUserDefined,


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    # bpy.app.handlers.frame_change_pre.append(
    #     randomise_camera_transform_per_frame
    # )

    print("transform operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # bpy.app.handlers.frame_change_pre.remove(
    #     randomise_camera_transform_per_frame
    # )

    print("transform operators unregistered")
