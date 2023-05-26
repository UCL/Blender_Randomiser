import bpy


# -------
# Panel
class PanelAddCustomProp(bpy.types.Panel):
    """Class defining the panel for randomising
    the camera transform

    """

    bl_idname = "CUSTOM_PROP_PT_random"
    bl_label = "Randomise CUSTOM"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        # Create a simple row.
        # Create an row where the buttons are aligned to each other.
        row = layout.row()
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)
        col5 = row_split.column(align=True)

        col1.label(text=" Randomise custom prop:")
        col2.label(text="")
        col3.label(text="min")
        col4.label(text="max")
        col5.label(text="index")

        ###################
        # Camera positon
        row = layout.row()  # row = layout.row(align=True)
        row.label(text="Enter Prop: ")

        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)
        col5 = row_split.column(align=True)

        # if context.scene.randomise_camera_props.bool_delta:
        #     value_str = "delta_location"
        # else:
        #     value_str = "location"

        col1.prop(context.scene.custom_props, "custom_input", text="")
        # col1.enabled = False

        # col1.label(context.scene.custom_props, "custom_input")
        # col1.enabled=True

        col2.prop(
            context.scene.custom_props,
            "custom_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.custom_props,
            "custom_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.custom_props,
            "custom_idx",
            icon_only=True,
        )

        col5.prop(
            context.scene.custom_props,
            "bool_rand_cust",
            icon_only=True,
        )

        # Bool delta
        col = self.layout.column()

        # Randomise button
        col.operator("opr.apply_random_custom_prop", text="Randomise")


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelAddCustomProp,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("custom UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("custom UI unregistered")
