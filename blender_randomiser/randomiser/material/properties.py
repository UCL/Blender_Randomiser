"""
An add-on to randomise the material parameters
of the selected objects

"""

import re

import bpy
import numpy as np

# ---------------------
# Python global vars
# TODO: use out.type=='VALUE', 'RGBA' instead? (type of the output socket)
# TODO: rethink this mapping....
# the idea is to map nodesocket types to property types I can use in the UI

MAP_SOCKET_TYPE_TO_ATTR = {
    bpy.types.NodeSocketFloat: "float_1d",
    bpy.types.NodeSocketVector: "float_3d",
    bpy.types.NodeSocketColor: "rgba_4d",  # "float_4d",
}

# NOTE: if the property is a float vector of size (1,3)
# the min/max values apply to all dimensions
# (these min/max values will be 'broadcasted' to the dimension specified in the
# attribute name)
MAP_SOCKET_TYPE_TO_INI_MIN_MAX = {
    bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketVector: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketColor: {"min": 0.0, "max": 1.0},
}

# TODO: eventually add option to read
# initial, min and max values from config file?


# -----------------------------------------
# Bounds to Socket properties
def constrain_min_closure(m_str):
    def constrain_min(self, context, m_str):
        # self is a 'SocketProperties' object
        # if min > max --> min is reset to max value
        # (i.e., no randomisation)
        min_array = np.array(getattr(self, "min_" + m_str))
        max_array = np.array(getattr(self, "max_" + m_str))
        if any(min_array > max_array):
            setattr(
                self,
                "min_" + m_str,
                np.where(min_array > max_array, max_array, min_array),
            )
        return

    return lambda slf, ctx: constrain_min(slf, ctx, m_str)


def constrain_max_closure(m_str):
    def constrain_max(self, context, m_str):
        # self is a 'SocketProperties' object
        # if max < min --> max is reset to min value
        # (i.e., no randomisation)
        min_array = np.array(getattr(self, "min_" + m_str))
        max_array = np.array(getattr(self, "max_" + m_str))
        if any(max_array < min_array):
            setattr(
                self,
                "max_" + m_str,
                np.where(max_array < min_array, min_array, max_array),
            )
        return

    return lambda slf, ctx: constrain_max(slf, ctx, m_str)


def constrain_rgba_closure(m_str):
    def constrain_rgba(self, context, min_or_max_full_str):
        # self is a 'SocketProperties' object
        # if RGBA socket: constrain values to be between 0 and 1
        min_or_max_array = np.array(getattr(self, min_or_max_full_str))
        if any(min_or_max_array > 1.0) or any(min_or_max_array < 0.0):
            setattr(
                self,
                min_or_max_full_str,
                np.clip(min_or_max_array, 0.0, 1.0),
            )
        return

    return lambda slf, ctx: constrain_rgba(slf, ctx, m_str)


# -----------------------
# Blender SocketProperties object
class SocketProperties(bpy.types.PropertyGroup):
    """
    Properties for a socket element

    Types of properties:---these relate to UI buttons
     bpy.props.
              BoolProperty(
              BoolVectorProperty(
              CollectionProperty(
              EnumProperty(
              FloatProperty(
              FloatVectorProperty(
              IntProperty(
              IntVectorProperty(
              PointerProperty(
              RemoveProperty(
              StringProperty(

    """

    # TODO: how to set attributes dynamically?
    # TODO: I don't get why this type def is also assignment

    # name (we can use it to access sockets in collection by name)
    name: bpy.props.StringProperty()  # type: ignore

    # float properties: they default to 0s
    # ---------------------
    ### float 1d
    float_1d_str = "float_1d"
    min_float_1d: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, update=constrain_min_closure(float_1d_str)
    )

    max_float_1d: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, update=constrain_max_closure(float_1d_str)
    )

    # ---------------------
    ### float 3d
    float_3d_str = "float_3d"
    min_float_3d: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_min_closure(float_3d_str)
    )
    max_float_3d: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_max_closure(float_3d_str)
    )

    # ---------------------
    ### float 4d
    float_4d_str = "float_4d"
    min_float_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4,
        update=constrain_min_closure(float_4d_str),
    )
    max_float_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4, update=constrain_max_closure(float_4d_str)
    )

    # ---------------------
    ### rgba
    # TODO: can this (rgba_4d_str...) be a bit more failsafe?
    # the update fn in this case clamps values between 0 and 1
    # (but this potentially limits range of values bc of single
    # float precision?)
    rgba_4d_str = "rgba_4d"
    min_rgba_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4,
        update=constrain_rgba_closure("min_" + rgba_4d_str),  # noqa
    )
    max_rgba_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4, update=constrain_rgba_closure("max_" + rgba_4d_str)  # noqa
    )

    # ---------------------
    ### bool
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# ------------------------------------
def get_candidate_sockets(self):
    # list input nodes
    list_input_nodes = [
        nd
        for nd in bpy.data.materials["Material"].node_tree.nodes
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random".lower())
    ]
    # list of sockets (eventually if linked?)
    list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
    return list_sockets


def get_update_collection(self):
    # Get fn for update_collection' property
    # It will run when the property value is 'get' and
    # it will update the *collection of socket properties* if required

    # set of sockets in collection
    set_of_sockets_in_collection_of_props = set(
        sck_p.name for sck_p in self.sockets2randomise_props
    )

    # set of sockets in graph
    set_of_sockets_in_graph = set(
        sck.node.name + "_" + sck.name for sck in self.candidate_sockets
    )
    collection_needs_update = (
        set_of_sockets_in_collection_of_props.symmetric_difference(
            set_of_sockets_in_graph
        )
    )

    # if there is a diff: overwrite the collection of sockets
    if collection_needs_update:
        set_update_collection(self, True)
        return True  # if returns True, it has been updated
    else:
        return False  # if returns False, it hasnt


def set_update_collection(self, value):
    # Set fn for the update_collection scene property
    # It will run when the property value is 'set'
    # It will overwrite the collection of socket properties
    if value:
        self.sockets2randomise_props.clear()  # ---ideally just update!
        for sckt in self.candidate_sockets:
            sckt_prop = self.sockets2randomise_props.add()
            sckt_prop.name = sckt.node.name + "_" + sckt.name
            sckt_prop.bool_randomise = True

            # ---------------------------
            # add min/max values
            # TODO: review - is this too hacky?
            # for this socket type, get the name of the attribute
            # holding the min/max properties
            socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                type(sckt)
            ]
            # for the shape of the array from the attribute name:
            # extract last number between '_' and 'd/D' in the attribute name
            n_dim = int(re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1])
            # ---------------------------

            # get dict with initial min/max values for this socket type
            ini_min_max_values = bpy.context.scene.socket_type_to_ini_min_max[
                type(sckt)
            ]

            # assign
            for m_str in ["min", "max"]:
                setattr(
                    sckt_prop,
                    m_str + "_" + socket_attrib_str,
                    (ini_min_max_values[m_str],) * n_dim,
                )
        # return True


# -----
list_classes_to_register = [
    SocketProperties,
]


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(SocketProperties)

        # add the collection of socket properties
        # to bpy.context.scene
        if cls == SocketProperties:
            bp = bpy.props
            bpy.types.Scene.sockets2randomise_props = bp.CollectionProperty(
                type=SocketProperties  # type of the elements in the collection
            )

    # link global Python variables to context.scene
    setattr(bpy.types.Scene, "socket_type_to_attr", MAP_SOCKET_TYPE_TO_ATTR)
    setattr(
        bpy.types.Scene,
        "socket_type_to_ini_min_max",
        MAP_SOCKET_TYPE_TO_INI_MIN_MAX,
    )

    # Define candidate sockets as a Python managed property
    # 'bpy.context.scene.candidate_sockets' will provide an updated list of
    # candidate sockets
    bpy.types.Scene.candidate_sockets = property(fget=get_candidate_sockets)

    # Define 'update_collection_socket_props' as a boolean Blender prop
    # we define custom get() and set() functions that trigger updates in the
    # collection of socket properties
    bpy.types.Scene.update_collection_socket_props = bpy.props.BoolProperty(
        default=False,  # initial value
        get=get_update_collection,  # get_update_materials;
        # this fn is called when
        # bpy.context.scene.update_collection_socket_props
        set=set_update_collection,  # set_update_materials;
        # this fn is called when
        # bpy.context.scene.update_collection_socket_props = 'patata'
        name="Update collection of socket properties",
    )
    # if I 'get' this property: it will update if required
    #   > bpy.context.scene.update_collection_socket_props
    # if I set this property to True: it will force an update
    #   >  bpy.context.scene.update_collection_socket_props = True

    print("material properties registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete global Python vars
    delattr(bpy.types.Scene, "socket_type_to_attr")
    delattr(bpy.types.Scene, "socket_type_to_ini_min_max")

    # delete the custom properties
    del bpy.types.Scene.sockets2randomise_props
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="sockets2randomise_props"
    )

    del bpy.types.Scene.candidate_sockets
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="candidate_sockets"
    )

    del bpy.types.Scene.update_collection_socket_props
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="update_collection_socket_props"
    )

    print("material properties unregistered")
