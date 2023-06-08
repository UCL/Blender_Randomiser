import bpy

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

list_context_scene_attr = ["socket_type_to_attr"]


def register():
    collection_UD_socket_properties.register()
    collection_UD_props.register()

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

    print("UD properties unregistered")
