import bpy


class CUSTOM_UL_items(bpy.types.UIList):
    def draw_item(
        self,
        context,
        layout,
        data,
        item,
        icon,
        active_data,
        active_propname,
        index,
    ):
        split = layout.split(factor=0.3)
        split.label(text="Index: %d" % (index))
        custom_icon = "COLOR"
        split.prop(item, "name", icon=custom_icon, emboss=False, text="")

    def invoke(self, context, event):
        pass


# class CUSTOM_PT_objectList(Panel):


# -------
# Panel
# -------
class PanelUserDefined(bpy.types.Panel):
    """Class defining the panel for the
    randomisation seed

    """

    bl_idname = "User_Defined_PT_Properties"
    bl_label = "Random user defined"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list(
            "CUSTOM_UL_items",
            "",
            scn,
            "custom",
            scn,
            "custom_index",
            rows=rows,
        )

        col = row.column(align=True)
        col.operator(
            "custom.list_action", icon="ZOOM_IN", text=""
        ).action = "ADD"
        col.operator(
            "custom.list_action", icon="ZOOM_OUT", text=""
        ).action = "REMOVE"
        col.separator()
        col.operator(
            "custom.list_action", icon="TRIA_UP", text=""
        ).action = "UP"
        col.operator(
            "custom.list_action", icon="TRIA_DOWN", text=""
        ).action = "DOWN"

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator(
            "custom.print_items", icon="LINENUMBERS_ON"
        )  # LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")

        # left_col_row.prop(
        #     context.scene.user_defined,
        # "Type property to randomise", icon_only=True
        # )
        # left_col_row.label(text="Choose property to randomise")


# -----------------------
# Classes to register
# -----------------------
list_classes_to_register = [
    CUSTOM_UL_items,
    PanelUserDefined,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("User Defined UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("User Defined UI unregistered")
