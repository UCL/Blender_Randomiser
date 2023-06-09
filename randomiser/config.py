# Parameters shared across materials modules
import bpy
import numpy as np
from mathutils import Vector

# MAX_NUMBER_OF_SUBPANELS: upper limit for the expected
# number of *materials* in a scene.
# This number of subpanels will be defined as classes, but
# only those panels with index < total number of materials
# will be displayed.
MAX_NUMBER_OF_SUBPANELS = 100

# MAX_NUMBER_OF_SUBSUBPANELS: upper limit for the expected
# number of *group nodes in a single material*.
# A total of MAX_NUMBER_OF_SUBPANELS*MAX_NUMBER_OF_SUBSUBPANELS subsubpanels
# will be defined as classes, but only those panels with
# index < total number of group nodes per material
# will be displayed.
MAX_NUMBER_OF_SUBSUBPANELS = 100


# Keyword to search for in nodes' names, to identify nodes to randomise
# case insensitive
DEFAULT_RANDOM_KEYWORD = "random"


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
    bpy.types.NodeSocketInt: "int_1d",
    bpy.types.NodeSocketBool: "bool_1d",
}

MAP_PROPS_TO_ATTR = {
    # bpy.types.NodeSocketFloat: "float_1d"
    # bpy.props.FloatVectorProperty size=1,
    Vector: "float_3d",  # bpy.props.FloatVectorProperty size=3,
    # bpy.types.NodeSocketInt: "int_1d"
    # bpy.props.IntProperty,
    # bpy.types.NodeSocketColor: "rgba_4d",  # "float_4d", if
    # bpy.types.NodeSocketBool: "bool_1d", elif
}

MAP_PROPS_TO_INI_MIN_MAX = {
    # bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    Vector: {"min": -np.inf, "max": np.inf},
    # bpy.types.NodeSocketInt: {
    #     "min": int(-1000),  # -2147483648
    #     "max": int(1000),  # 2147483647
    # },  # ---- not sure this will work?
}

# NOTE: if the property is a float vector of size (1,n)
# the initial min/max values specified here apply to all n dimensions
# TODO: should we change this to allow different values per dimension?
# (in that case the mapping should probably be from attribute name)
MAP_SOCKET_TYPE_TO_INI_MIN_MAX = {
    bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketVector: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketColor: {"min": 0.0, "max": 1.0},
    bpy.types.NodeSocketInt: {
        "min": int(-1000),  # -2147483648
        "max": int(1000),  # 2147483647
    },  # ---- not sure this will work?
    bpy.types.NodeSocketBool: {"min": False, "max": True},
}
