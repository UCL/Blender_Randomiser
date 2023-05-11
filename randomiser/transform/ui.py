import bpy


# -------
# Panel
class PanelAddRandomTransform(bpy.types.Panel):
    """Class defining the panel for randomising
    the camera transform

    """

    bl_idname = "NODE_MATERIAL_PT_random_transform"
    bl_label = "Randomise TRANSFORM"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        col = self.layout.column()
        row = col.row()
        row.prop(
            context.scene.randomise_camera_props,
            "bool_delta",
        )

        col.operator("opr.apply_random_transform", text="Randomize")

        layout = self.layout

        # Create a simple row.
        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Randomise position:")
        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_min",
        )
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_max",
        )

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_min",
        )
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_max",
        )

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_min",
        )
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_max",
        )

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Rotation x:")
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_min",
        )
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_max",
        )

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Rotation y:")
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_min",
        )
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_max",
        )

        # Third column, aligned
        col = split.column(align=True)
        col.label(text="Rotation z:")
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_min",
        )
        col.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_max",
        )


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelAddRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("transform UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("transform UI unregistered")
