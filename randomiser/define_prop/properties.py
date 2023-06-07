import bpy

from .property_classes import (
    collection_UD_socket_properties,
)

# ---------------------------
# Properties
# class PropertiesCustomTransform(bpy.types.PropertyGroup):
#     """
#     Class holding the set of properties
#     for the camera position and rotation:
#     - min/max values for x/y/z component of position and rotation, and
#     - boolean for delta position and rotation
#     - boolean for setting seed value
#     - integer for the actual seed value

#     """

#     # Position min and max values
#     custom_input_prop = bpy.props.StringProperty(name="enter text")
#     custom_input: custom_input_prop  # type: ignore
#     custom_min: bpy.props.FloatVectorProperty(  # type: ignore
#         size=1,
#         step=100,  # update=constrain_min_closure(custom_input)
#     )  # type: ignore
#     custom_max: bpy.props.FloatVectorProperty(  # type: ignore
#         size=1,
#         step=100,  # update=constrain_max_closure(custom_input)
#     )  # type: ignore
#     custom_idx: bpy.props.IntProperty(default=0)  # type: ignore

#     # BOOL
#     bool_rand_cust: bpy.props.BoolProperty(default=True)  # type: ignore


class PropertiesCustomList(bpy.types.PropertyGroup):
    custom_string_prop = bpy.props.StringProperty(default="camera.location")
    custom_string: custom_string_prop  # type: ignore


custom_string_prop = bpy.props.StringProperty(default="camera.location")


class CUSTOM_colorCollection(bpy.types.PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    id_prop = bpy.props.IntProperty()
    id: id_prop  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    # PropertiesCustomTransform,
    PropertiesCustomList,
    CUSTOM_colorCollection,
]

list_context_scene_attr = ["socket_type_to_attr"]


def register():
    collection_UD_socket_properties.register()

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # if cls == PropertiesCustomTransform:
        #     bpy.types.Scene.custom_props = bpy.props.PointerProperty(
        #         type=PropertiesCustomTransform
        #     )

        if cls == PropertiesCustomList:
            bpy.types.Scene.custom_list = bpy.props.PointerProperty(
                type=PropertiesCustomList
            )

        for attr, attr_val in zip(
            list_context_scene_attr,
            [custom_string_prop],
        ):
            setattr(bpy.types.Scene, attr, attr_val)

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

    # del bpy.types.Scene.custom_props
    del bpy.types.Scene.custom_list

    # delete the custom properties linked to bpy.context.scene
    for attr in list_context_scene_attr:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

    print("UD properties unregistered")
