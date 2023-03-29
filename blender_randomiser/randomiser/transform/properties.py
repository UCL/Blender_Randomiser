import bpy
import numpy as np
import pdb
from mathutils import Vector


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
    camera_pos: bpy.props.FloatVectorProperty(size=3,step=100,)  # type: ignore
    camera_rot: bpy.props.FloatVectorProperty(size=3,step=100,)  # type: ignore

    # min_float_3d: bpy.props.FloatVectorProperty()  # type: ignore
    # max_float_3d: bpy.props.FloatVectorProperty()  # type: ignore

    # min_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore
    # max_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore

    # BOOL
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
        # add custom props to the scene! before registering the rest?
        if cls == PropertiesApplyRandomTransform:
            bpy.types.Scene.randomise_camera_props = (
                bpy.props.PointerProperty(
                    type=PropertiesApplyRandomTransform
                )
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


def randomize_selected(context, #seed, delta,
                       loc, rot, randomise_on):

    import random
    from random import uniform

    # random.seed(seed)

    def rand_vec(vec_range):
        return Vector(uniform(-val, val) for val in vec_range)
    
    

    for obj in context.selected_objects:

        if loc:
            obj.location += rand_vec(loc)
            #pdb.set_trace()
            # if delta:
            #     obj.delta_location += rand_vec(loc)
            # else:
            #     obj.location += rand_vec(loc)
        else:  # otherwise the values change under us
            uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)

        if rot:
            vec = rand_vec(rot)

            rotation_mode = obj.rotation_mode
            if rotation_mode in {'QUATERNION', 'AXIS_ANGLE'}:
                obj.rotation_mode = 'XYZ'

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
