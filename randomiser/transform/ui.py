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
        layout.label(text=" Randomise camera position:")
        row = layout.row()  # row = layout.row(align=True)
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_min",
            icon_only=True,
        )
        row.label(text="x_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_max",
            icon_only=True,
        )
        row.label(text="x_max")

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_min",
            icon_only=True,
        )
        row.label(text="y_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_max",
            icon_only=True,
        )
        row.label(text="y_max")

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_min",
            icon_only=True,
        )
        row.label(text="z_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_max",
            icon_only=True,
        )
        row.label(text="z_max")

        # Rotation part of panel
        layout.label(text=" Randomise camera rotation:")
        row = layout.row()  # row = layout.row(align=True)
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_min",
            icon_only=True,
        )
        row.label(text="x_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_max",
            icon_only=True,
        )
        row.label(text="x_max")

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_min",
            icon_only=True,
        )
        row.label(text="y_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_max",
            icon_only=True,
        )
        row.label(text="y_max")

        row = layout.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_min",
            icon_only=True,
        )
        row.label(text="z_min")

        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_max",
            icon_only=True,
        )
        row.label(text="z_max")

        # Seed
        row = self.layout.row(align=True)
        split = row.split()
        left_col = split.column(align=True)
        right_col = split.column(align=True)

        # put the toggle on the left col
        left_col_row = left_col.row(align=True)
        left_col_row.alignment = "RIGHT"  # alignment first!
        left_col_row.prop(
            context.scene.randomise_camera_props, "seed_toggle", icon_only=True
        )
        left_col_row.label(text="Set random seed")

        # put field in right col
        right_col.enabled = (
            context.scene.randomise_camera_props.seed_toggle
        )  # only disable the next part of the row
        right_col.prop(context.scene.randomise_camera_props, "seed")


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
