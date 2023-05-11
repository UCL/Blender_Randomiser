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
        layout = self.layout

        # Create a simple row.
        # Create an row where the buttons are aligned to each other.
        row = layout.row()  # row = layout.row(align=True)
        row.label(text=" Randomise camera position:")
        row.label(text="min")
        row.label(text="max")

        row = layout.row()  # row = layout.row(align=True)
        row.label(text="x_position")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_max",
            icon_only=True,
        )

        row = layout.row()
        row.label(text="y_position")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_max",
            icon_only=True,
        )

        row = layout.row()
        row.label(text="z_position")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_max",
            icon_only=True,
        )

        # Rotation part of panel
        layout.label(text=" Randomise camera rotation:")
        row = layout.row()  # row = layout.row(align=True)
        row.label(text="x_rotation")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_max",
            icon_only=True,
        )

        row = layout.row()
        row.label(text="y_rotation")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_max",
            icon_only=True,
        )

        row = layout.row()
        row.label(text="x_rotation")
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_min",
            icon_only=True,
        )

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_max",
            icon_only=True,
        )

        col = self.layout.column()
        row = col.row()
        row.prop(
            context.scene.randomise_camera_props,
            "bool_delta",
        )

        col.operator("opr.apply_random_transform", text="Randomize")


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelAddRandomTransform,
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
