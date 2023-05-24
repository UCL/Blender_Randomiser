import bpy

from .. import config
from .property_classes import (
    collection_materials,
    collection_socket_properties,
    socket_properties,
)

# ------------------------------------
# Register / unregister classes
# ------------------------------------
dict_context_scene_attr = {
    "socket_type_to_attr": config.MAP_SOCKET_TYPE_TO_ATTR,
    "socket_type_to_ini_min_max": config.MAP_SOCKET_TYPE_TO_INI_MIN_MAX,
}


def register():
    socket_properties.register()
    collection_socket_properties.register()
    collection_materials.register()

    # link global Python variables to bpy.context.scene
    # if I use setattr: attribute must exist first right?
    for attr_ky, attr_val in dict_context_scene_attr.items():
        setattr(bpy.types.Scene, attr_ky, attr_val)

    print("material properties registered")


def unregister():
    socket_properties.unregister()
    collection_socket_properties.unregister()
    collection_materials.unregister()

    # delete the custom properties linked to bpy.context.scene
    for attr_ky in dict_context_scene_attr.keys():
        if hasattr(bpy.types.Scene, attr_ky):
            delattr(bpy.types.Scene, attr_ky)

    print("material properties unregistered")
