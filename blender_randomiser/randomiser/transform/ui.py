import bpy
import numpy as np
import pdb



# -------
# Panel
class PanelAddRandomTransform(bpy.types.Panel):
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
        row.prop(context.scene.randomise_camera_props, 'camera_pos',)
        row = col.row()
        row.prop(context.scene.randomise_camera_props, 'camera_rot',)
        row = col.row()
        row.prop(context.scene.randomise_camera_props, 'bool_delta',)
        # for (prop_name, _) in PROPS:
        #     row = col.row()
        #     # if prop_name == 'camera_pos':
        #     #     row = row.row()
        #     #     row.enabled = context.scene.randomise_camera_pos
        #     # elif prop_name == 'rotation':
        #     #     row = row.row()
        #     #     row.enabled = context.scene.randomise_rotation
        #     row.prop(context.scene, prop_name)

        col.operator('opr.apply_random_transform', text='Randomize')
        ##### do we need this to randomise or to apply transform?????
        # Randomize_transform updates automatically every time you change the random seed

        layout = self.layout
        scene = context.scene

        # Create a simple row.
        # Create an row where the buttons are aligned to each other.

        layout.label(text=" Randomise position:")
        row = layout.row() #row = layout.row(align=True)
        row.prop(context.scene.randomise_camera_props, 'camera_pos_x_min',)
        row.prop(context.scene.randomise_camera_props, 'camera_pos_x_max',)

        #layout.label(text=" Randomise position y:")
        row = layout.row()
        row.prop(context.scene.randomise_camera_props, 'camera_pos_y_min',)
        row.prop(context.scene.randomise_camera_props, 'camera_pos_y_max',)

        #layout.label(text=" Randomise position z:")
        row = layout.row()
        row.prop(context.scene.randomise_camera_props, 'camera_pos_z_min',)
        row.prop(context.scene.randomise_camera_props, 'camera_pos_z_max',)



        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Rotation x:")
        col.prop(context.scene.randomise_camera_props, 'camera_rot_x_min',)
        col.prop(context.scene.randomise_camera_props, 'camera_rot_x_max',)

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Rotation y:")
        col.prop(context.scene.randomise_camera_props, 'camera_rot_y_min',)
        col.prop(context.scene.randomise_camera_props, 'camera_rot_y_max',)

        # Third column, aligned
        col = split.column(align=True)
        col.label(text="Rotation z:")
        col.prop(context.scene.randomise_camera_props, 'camera_rot_z_min',)
        col.prop(context.scene.randomise_camera_props, 'camera_rot_z_max',)
        
        # # Big render button
        # layout.label(text="Big Button:")
        # row = layout.row()
        # row.scale_y = 3.0
        # row.operator("render.render")

        # # Different sizes in a row
        # layout.label(text="Different button sizes:")
        # row = layout.row(align=True)
        # row.operator("render.render")

        # sub = row.row()
        # sub.scale_x = 2.0
        # sub.operator("render.render")

        # row.operator("render.render")

# PROPS = [
#     # ('random_seed', bpy.props.IntProperty(name='Random Seed', default=0)),
#     #('randomise_camera_pos', bpy.props.BoolProperty(name='Randomize camera_pos', default=False))
#     ('camera_pos', bpy.props.FloatProperty(name='Camera camera_pos', default=[0,0,0])),
#     #('randomise_rotation', bpy.props.BoolProperty(name='Randomize Rotation', default=False))
#     ('rotation', bpy.props.FloatProperty(name='Camera Rotation', default=[0,0,0])),
# ]


# #-------------------------------
# Define function to append operator to menu's methods
# def menu_func(self, context):
#     # self.layout is a bpy.types.UILayout
#     # operator:
#     # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.operator
#     self.layout.operator(AddRandomCube.bl_idname)


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