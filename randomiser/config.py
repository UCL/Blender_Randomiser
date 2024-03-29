# Parameters shared across materials modules
import bpy
import numpy as np
from mathutils import Euler, Vector

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
# - the idea is to map nodesocket types to property types I can use in the UI
# - the way I infer the dimension of the float vector is not ideal
MAP_SOCKET_TYPE_TO_ATTR = {
    bpy.types.NodeSocketFloat: "float_1d",
    bpy.types.NodeSocketVector: "float_3d",
    bpy.types.NodeSocketColor: "rgba_4d",
    bpy.types.NodeSocketInt: "int_1d",
    bpy.types.NodeSocketBool: "bool_1d",
}

# NOTE: if the property is a float vector of size (1,n)
# the initial min/max values specified here apply to all n dimensions
MAP_SOCKET_TYPE_TO_INI_MIN_MAX = {
    bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketVector: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketColor: {"min": 0.0, "max": 1.0},
    bpy.types.NodeSocketInt: {
        "min": int(-2147483648),
        "max": int(2147483647),
    },
    bpy.types.NodeSocketBool: {"min": False, "max": True},
}

# NOTE: Mapping for user defined properties
MAP_PROPS_TO_ATTR = {
    Vector: "float_3d",
    float: "float_1d",
    int: "int_1d",
    bool: "bool_1d",
    Euler: "euler",
}

MAP_PROPS_TO_INI_MIN_MAX = {
    Vector: {"min": -np.inf, "max": np.inf},
    float: {"min": -np.inf, "max": np.inf},
    int: {"min": int(-2147483648), "max": int(2147483647)},
    bool: {"min": False, "max": True},
    Euler: {"min": -np.inf, "max": np.inf},
}
