"""
An add-on to randomise location,
rotation and scale of the selected objects

"""
### Imports

import bpy
from mathutils import Vector

# bpy.data.objects['Camera'].location[0-2]
# bpy.data.objects['Camera'].rotation_euler[0-2]
# bpy.context.camera


# ---------------------------
# Properties
class PropertiesApplyRandomTransform(
    bpy.types.PropertyGroup
):  # ---these will be added to context.scene.<custom_prop> in registration
    # camera_rot_prop = bpy.props.FloatProperty(
    #     name="Camera camera_rot",
    #     default=0.0,
    #     soft_min=-50.0,
    #     soft_max=50.0,
    #     step=100,
    # )  # OJO in step: the actual value is the value set here divided by 100

    # seed_toggle_prop = bpy.props.BoolProperty(
    #     name="Set random seed", default=False
    # )
    # seed_toggle: seed_toggle_prop  # type: ignore

    # seed_prop = bpy.props.IntProperty(name="Seed", default=42)
    # seed: seed_prop  # type: ignore

    # float props: defaults to 0s
    # camera_rot: camera_rot_prop  # type: ignore
    camera_pos: bpy.props.FloatVectorProperty(  # type: ignore
        size=3,
        step=100,
    )
    camera_rot: bpy.props.FloatVectorProperty(  # type: ignore
        size=3,
        step=100,
    )

    # min_float_3d: bpy.props.FloatVectorProperty()  # type: ignore
    # max_float_3d: bpy.props.FloatVectorProperty()  # type: ignore

    # min_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore
    # max_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore

    # BOOL
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# -------------------------------
## Operators
class ApplyRandomTransform(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Add a random cube within a predefined volume"""

    bl_idname = "opr.apply_random_transform"  # appended to bpy.ops.
    bl_label = "Apply random transform to object"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current context
    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    # ----------------------
    ## Invoke
    # runs before execute, to initialise ....?
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        loc = context.scene.randomise_camera_props.camera_pos
        rot = context.scene.randomise_camera_props.camera_rot
        randomise_on = True

        randomize_selected(context, loc, rot, randomise_on)

        # # for obj in bpy.context.selected_objects:
        # #     rename_object(obj, params)

        # # add a cube primitive and link it to the scene collection
        # bpy.ops.mesh.primitive_uv_sphere_add()
        # # returns {'FINISHED'} if successful
        # cube_object = context.object

        # # get inputs
        # # seed:
        # If None, fresh unpredictable entropy will be pulled from the OS
        # scene = context.scene
        # seed = (
        #     scene.random_cube_props.seed
        #     if scene.random_cube_props.seed_toggle
        #     else None
        # )
        # vol_size = scene.random_cube_props.vol_size

        # # set location randomly within predifined volume
        # rng = np.random.default_rng(
        #     seed
        # )  # recommended constructor for the random number class Generator
        # cube_object.location = vol_size * rng.random((3,)) - 0.5 * vol_size

        return {"FINISHED"}


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
        row.prop(
            context.scene.randomise_camera_props,
            "camera_pos",
        )
        row = col.row()
        row.prop(
            context.scene.randomise_camera_props,
            "camera_rot",
        )
        row = col.row()
        row.prop(
            context.scene.randomise_camera_props,
            "bool_randomise",
        )
        # for (prop_name, _) in PROPS:
        #     row = col.row()
        #     # if prop_name == 'camera_pos':
        #     #     row = row.row()
        #     #     row.enabled = context.scene.randomise_camera_pos
        #     # elif prop_name == 'rotation':
        #     #     row = row.row()
        #     #     row.enabled = context.scene.randomise_rotation
        #     row.prop(context.scene, prop_name)

        col.operator("opr.apply_random_transform", text="Randomize")
        ##### do we need this to randomise or to apply transform?????
        # Randomize_transform updates automatically
        # every time you change the random seed

        layout = self.layout

        scene = context.scene
        # Create a simple row.
        # self.layout(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")


# PROPS = [
#     # ('random_seed',
# bpy.props.IntProperty(name='Random Seed', default=0)),
#     #('randomise_camera_pos',
# bpy.props.BoolProperty(name='Randomize camera_pos', default=False))
#     ('camera_pos',
# bpy.props.FloatProperty(name='Camera camera_pos', default=[0,0,0])),
#     #('randomise_rotation',
# bpy.props.BoolProperty(name='Randomize Rotation', default=False))
#     ('rotation',
# bpy.props.FloatProperty(name='Camera Rotation', default=[0,0,0])),
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
    PropertiesApplyRandomTransform,
    PanelAddRandomTransform,
    ApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
        # add custom props to the scene! before registering the rest?
        if cls == PropertiesApplyRandomTransform:
            bpy.types.Scene.randomise_camera_props = bpy.props.PointerProperty(
                type=PropertiesApplyRandomTransform
            )
            # alternative: setattr(bpy.types.Scene, prop_name, prop_value)?

    # Adds the new operator to an existing menu.
    # bpy.types.VIEW3D_MT_object.append(menu_func)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete the custom property pointer
    # NOTE: this is different from its accessor, as that is a read/write only
    # to delete this we have to delete its pointer, just like how we added it
    # delattr(bpy.types.Scene, 'randomise_camera_props')
    # del bpy.types.Scene.randomise_camera_props
    # bpy.ops.wm.properties_remove(
    #     data_path="scene", property_name="randomise_camera_props"
    # )

    del bpy.types.Scene.randomise_camera_props
    # Remove the operator from existing menu.
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    print("unregistered")


def randomize_selected(context, loc, rot, randomise_on):  # seed, delta,
    from random import uniform

    # random.seed(seed)

    def rand_vec(vec_range):
        return Vector(uniform(-val, val) for val in vec_range)

    for obj in context.selected_objects:
        if loc:
            obj.location += rand_vec(loc)
            # pdb.set_trace()
            # if delta:
            #     obj.delta_location += rand_vec(loc)
            # else:
            #     obj.location += rand_vec(loc)
        else:  # otherwise the values change under us
            uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)

        if rot:
            vec = rand_vec(rot)

            rotation_mode = obj.rotation_mode
            if rotation_mode in {"QUATERNION", "AXIS_ANGLE"}:
                obj.rotation_mode = "XYZ"

            obj.rotation_euler[0] += vec[0]
            obj.rotation_euler[1] += vec[1]
            obj.rotation_euler[2] += vec[2]

            # if delta:
            #     obj.delta_rotation_euler[0] += vec[0]
            #     obj.delta_rotation_euler[1] += vec[1]
            #     obj.delta_rotation_euler[2] += vec[2]
            # else:
            #     obj.rotation_euler[0] += vec[0]
            #     obj.rotation_euler[1] += vec[1]
            #     obj.rotation_euler[2] += vec[2]
            obj.rotation_mode = rotation_mode
        else:
            uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)
