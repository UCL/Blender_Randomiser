import bpy
import numpy as np

from .collection_socket_properties import ColSocketProperties
from .socket_properties import SocketProperties

# ---------------------
# Python global vars
# ---------------------
# TODO: use out.type=='VALUE', 'RGBA' instead? (type of the output socket)
# TODO: rethink this mapping....
# - the idea is to map nodesocket types to property types I can use in the UI
# - the way I infer the dimension of the float vector is not ideal
MAP_SOCKET_TYPE_TO_ATTR = {
    bpy.types.NodeSocketFloat: "float_1d",
    bpy.types.NodeSocketVector: "float_3d",
    bpy.types.NodeSocketColor: "rgba_4d",  # "float_4d",
}

# NOTE: if the property is a float vector of size (1,n)
# the initial min/max values specified here apply to all n dimensions
# TODO: should we change this to allow different values per dimension?
# (in that case the mapping should probably be from attribute name)
MAP_SOCKET_TYPE_TO_INI_MIN_MAX = {
    bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketVector: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketColor: {"min": 0.0, "max": 1.0},
}


# ------------------------------------
# Register / unregister classes
# ------------------------------------
list_classes_to_register = [
    SocketProperties,
    ColSocketProperties,
]


def register():
    # register classes
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # add the collection of socket properties
        # to bpy.context.scene
        if cls == ColSocketProperties:
            bp = bpy.props
            bpy.types.Scene.socket_props_per_material = bp.CollectionProperty(
                type=ColSocketProperties
            )

    # link global Python variables to bpy.context.scene
    # if I use setattr: attribute must exist first right?
    for attr, attr_val in zip(
        ["socket_type_to_attr", "socket_type_to_ini_min_max"],
        [MAP_SOCKET_TYPE_TO_ATTR, MAP_SOCKET_TYPE_TO_INI_MIN_MAX],
    ):
        setattr(bpy.types.Scene, attr, attr_val)

    print("material properties registered")


def unregister():
    # unregister classes
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete the custom properties linked to bpy.context.scene
    list_attr = [
        "socket_type_to_attr",
        "socket_type_to_ini_min_max",
        "socket_props_per_material",
    ]
    for attr in list_attr:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    print("material properties unregistered")
