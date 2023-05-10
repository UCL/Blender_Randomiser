import bpy


# ---------------------------
# Properties
class PropertiesApplyRandomSeed(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for the camera position and rotation:
    - min/max values for x/y/z component of position and rotation, and
    - boolean for delta position and rotation
    - boolean for setting seed value
    - integer for the actual seed value

    """

    seed_toggle_prop = bpy.props.BoolProperty(
        name="Set random seed", default=False
    )
    seed_toggle: seed_toggle_prop  # type: ignore

    seed_prop = bpy.props.IntProperty(name="Seed", default=42)
    seed: seed_prop  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesApplyRandomSeed,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        bpy.types.Scene.seed_properties = bpy.props.PointerProperty(
            type=PropertiesApplyRandomSeed
        )  # bpy.context.scene.seed_properties.seed

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.seed_properties

    print("unregistered")
