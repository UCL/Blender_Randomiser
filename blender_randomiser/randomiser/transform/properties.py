import bpy


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
    )  # type: ignore
    camera_rot: bpy.props.FloatVectorProperty(  # type: ignore
        size=3,
        step=100,
    )  # type: ignore
    camera_pos_x_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_pos_x_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_pos_y_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_pos_y_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_pos_z_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_pos_z_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore

    camera_rot_x_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_rot_x_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_rot_y_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_rot_y_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_rot_z_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore
    camera_rot_z_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,
    )  # type: ignore

    # BOOL
    bool_delta: bpy.props.BoolProperty()  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        if cls == PropertiesApplyRandomTransform:
            bpy.types.Scene.randomise_camera_props = bpy.props.PointerProperty(
                type=PropertiesApplyRandomTransform
            )

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.randomise_camera_props

    print("unregistered")
