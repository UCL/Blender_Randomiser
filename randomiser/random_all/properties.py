import bpy


# ---------------------------
# Properties
class PropertiesRandomAll(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for the randomise all panels

    """

    # seed_toggle_prop = bpy.props.BoolProperty(
    #     name="Set random seed", default=False
    # )
    # seed_toggle: seed_toggle_prop  # type: ignore

    tot_frame_no_prop = bpy.props.IntProperty(
        name="Total Frame Number", default=50
    )
    tot_frame_no: tot_frame_no_prop  # type: ignore

    # x_pos = bpy.props.GenericType()


# ------------------------------------
# Register / unregister classes
# ------------------------------------
list_classes_to_register = [
    PropertiesRandomAll,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        bpy.types.Scene.rand_all_properties = bpy.props.PointerProperty(
            type=PropertiesRandomAll
        )

    print("randomise all properties registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.rand_all_properties

    print("randomise all properties unregistered")
