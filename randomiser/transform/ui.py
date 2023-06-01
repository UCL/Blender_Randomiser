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
    # TODO: refactor this, take from ..material.ui import TemplatePanel?
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

        col1.label(text=" Randomise camera position:")
        col2.label(text="")
        col3.label(text="min")
        col4.label(text="max")
        col5.label(text="")

        ###################
        # Camera positon
        row = layout.row()  # row = layout.row(align=True)
        row.label(text="x")

        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        if context.scene.randomise_camera_props.bool_delta:
            value_str = "delta_location"
        else:
            value_str = "location"

        col1.prop(context.scene.camera, value_str, icon_only=True, index=0)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_pos_x_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_posx",
            icon_only=True,
        )

        # ------------------------------------
        # Camera position y
        row = layout.row()
        row.label(text="y")

        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        # Camera positon y
        col1.prop(context.scene.camera, value_str, icon_only=True, index=1)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_pos_y_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_posy",
            icon_only=True,
        )

        row = layout.row()
        row.label(text="z")

        # Camera position z
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        # Camera positon y
        col1.prop(context.scene.camera, value_str, icon_only=True, index=2)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_pos_z_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_posz",
            icon_only=True,
        )

        #########################
        # Rotation part of panel
        layout.label(text=" Randomise camera rotation:")
        row = layout.row()  # row = layout.row(align=True)
        row.label(text="x")

        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        # Camera rotation x
        if context.scene.randomise_camera_props.bool_delta:
            value_str = "delta_rotation_euler"
        else:
            value_str = "rotation_euler"

        col1.prop(context.scene.camera, value_str, icon_only=True, index=0)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_rot_x_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_rotx",
            icon_only=True,
        )

        # Camera rotation y
        row = layout.row()
        row.label(text="y")
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        col1.prop(context.scene.camera, value_str, icon_only=True, index=1)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_rot_y_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_roty",
            icon_only=True,
        )

        # Camera rotation z
        row = layout.row()
        row.label(text="z")
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)

        col1.prop(context.scene.camera, value_str, icon_only=True, index=2)
        col1.enabled = False

        col2.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_min",
            icon_only=True,
        )

        col3.prop(
            context.scene.randomise_camera_props,
            "camera_rot_z_max",
            icon_only=True,
        )

        col4.prop(
            context.scene.randomise_camera_props,
            "bool_rand_rotz",
            icon_only=True,
        )

        # Bool delta
        col = self.layout.column()
        row = col.row()
        row.prop(
            context.scene.randomise_camera_props,
            "bool_delta",
        )

        # Randomise button
        col.operator("camera.apply_random_transform", text="Randomise")


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
