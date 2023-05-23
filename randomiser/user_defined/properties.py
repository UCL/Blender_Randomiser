import bpy

# class CUSTOM_colorCollection(PropertyGroup):
#     #name: StringProperty() -> Instantiated by default
#     id: IntProperty()


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
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # Custom scene properties
        bpy.types.Scene.custom = bpy.props.CollectionProperty(
            type=PropertiesUserDefined
        )
        bpy.types.Scene.custom_index = bpy.props.IntProperty()

        # bpy.types.Scene.custom = bpy.props.PointerProperty(
        #     type=PropertiesUserDefined
        # )

    print("user defined properties registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.user_defined

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

    print("user defined unregistered")
