import bpy

from .property_classes import (
    collection_UD_socket_properties,
)


# ---------------------------
# Properties
class PropertiesUserDefined(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for the random seed

    """

    user_defined_prop = bpy.props.StringProperty()

    user_defined: user_defined_prop  # type: ignore


# ------------------------------------
# Register / unregister classes
# ------------------------------------
list_classes_to_register = [
    PropertiesUserDefined,
]


def register():
    collection_UD_socket_properties.register()

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # Custom scene properties
        bpy.types.Scene.custom = bpy.props.CollectionProperty(
            type=PropertiesUserDefined
        )
        bpy.types.Scene.custom_index = bpy.props.IntProperty()

    print("geometry properties registered")


def unregister():
    collection_UD_socket_properties.unregister()

    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.user_defined

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

    print("geometry properties unregistered")
