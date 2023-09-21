import bpy


# ---------------------------
# Properties
class PropertiesRandomSeed(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for the random seed

    """

    seed_toggle_prop = bpy.props.BoolProperty(
        name="Set random seed", default=False
    )
    seed_toggle: seed_toggle_prop  # type: ignore

    seed_prop = bpy.props.IntProperty(name="Seed", default=42)
    seed: seed_prop  # type: ignore

    seed_previous_prop = bpy.props.IntProperty(
        name="Seed Previous", default=42
    )
    seed_previous: seed_previous_prop  # type: ignore


# ------------------------------------
# Register / unregister classes
# ------------------------------------
list_classes_to_register = [
    PropertiesRandomSeed,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        bpy.types.Scene.seed_properties = bpy.props.PointerProperty(
            type=PropertiesRandomSeed
        )

    print("seed properties registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.seed_properties

    print("seed properties unregistered")
