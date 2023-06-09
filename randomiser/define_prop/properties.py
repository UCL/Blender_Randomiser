import bpy

from .. import config
from .property_classes import (
    collection_UD_props,
    collection_UD_socket_properties,
)


class CUSTOM_colorCollection(bpy.types.PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    id_prop = bpy.props.IntProperty()
    id: id_prop  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    CUSTOM_colorCollection,
]

dict_context_scene_attr = {
    "UD_prop_to_attr": config.MAP_PROPS_TO_ATTR,
    "UD_prop_to_ini_min_max": config.MAP_PROPS_TO_INI_MIN_MAX,
}


def register():
    collection_UD_socket_properties.register()
    collection_UD_props.register()

    # link global Python variables to bpy.context.scene
    # if I use setattr: attribute must exist first right?
    for attr_ky, attr_val in dict_context_scene_attr.items():
        setattr(bpy.types.Scene, attr_ky, attr_val)

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # Custom scene properties
        if cls == CUSTOM_colorCollection:
            bpy.types.Scene.custom = bpy.props.CollectionProperty(
                type=CUSTOM_colorCollection
            )
        bpy.types.Scene.custom_index = bpy.props.IntProperty()

    print("UD properties registered")


def unregister():
    collection_UD_socket_properties.unregister()

    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

    # delete the custom properties linked to bpy.context.scene
    for attr_ky in dict_context_scene_attr.keys():
        if hasattr(bpy.types.Scene, attr_ky):
            delattr(bpy.types.Scene, attr_ky)

    print("UD properties unregistered")
