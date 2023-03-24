import re

import bpy
import numpy as np

from .. import utils

# ---------------------
# Python global vars
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


# -----------------------------------------
# Bounds to SocketProperties
# -----------------------------------------
def constrain_min_closure(m_str):
    """Constain min value with closure

    Parameters
    ----------
    m_str : str
            string specifying the socket attribute (e.g., float_1d)

    Returns
    -------
    _type_
        lambda function evaluated at the specified m_str

    """

    def constrain_min(self, context, m_str):
        """Constrain min value

        If min > max --> min is reset to max value
        (i.e., no randomisation)

        Parameters
        ----------
        context : _type_
            _description_
        m_str : str
            string specifying the socket attribute (e.g., float_1d)
        """
        # self is a 'SocketProperties' object
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
    """Constain max value with closure

    Parameters
    ----------
    m_str : str
        string specifying the socket attribute (e.g., float_1d)

    Returns
    -------
    _type_
        lambda function evaluated at the specified m_str

    """

    def constrain_max(self, context, m_str):
        """Constrain max value

        if max < min --> max is reset to min value
        (i.e., no randomisation)

        Parameters
        ----------
        context : _type_
            _description_
        m_str : str
            string specifying the socket attribute (e.g., float_1d)
        """
        # self is a 'SocketProperties' object
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
    """Constain RGBA value with closure

    Parameters
    ----------
    m_str : str
        string specifying the socket attribute (e.g., float_1d)

    Returns
    -------
    _type_
        lambda function evaluated at the specified m_str

    """

    def constrain_rgba(self, context, min_or_max_full_str):
        """Constrain RGBA value

        if RGBA socket: constrain values to be between 0 and 1

        Parameters
        ----------
        context : _type_
            _description_
        m_str : str
            string specifying the socket attribute (e.g., float_1d)
        """
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
# SocketProperties
# ---------------------
class SocketProperties(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for a socket, namely:
    - socket name,
    - min/max values, and
    - boolean for randomisation

    Because it is not possible to define attributes dynamically,
    for now we define an attribute for each possible socket type
    in the input nodes. These are all FloatVectors of different sizes.
    The size is specified in the attribute's name:
    - min/max_float_1d
    - min/max_float_3d
    - min/max_float_4d
    - min/max_rgba_4d

    """

    # TODO: how to set attributes dynamically?
    # TODO: I don't really get why this type definition is also assignment

    # ---------------------
    # name
    # NOTE: if we make a collection of this type of objects,
    # we can access them by name
    name: bpy.props.StringProperty()  # type: ignore

    # TODO: include the socket itself here to?
    # socket: PointerProperty(type=bpy.types.NodeSocketStandard?)

    # ---------------------
    # float 1d
    float_1d_str = "float_1d"
    min_float_1d: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, update=constrain_min_closure(float_1d_str)
    )

    max_float_1d: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, update=constrain_max_closure(float_1d_str)
    )

    # ---------------------
    # float 3d
    float_3d_str = "float_3d"
    min_float_3d: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_min_closure(float_3d_str)
    )
    max_float_3d: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_max_closure(float_3d_str)
    )

    # ---------------------
    # float 4d
    float_4d_str = "float_4d"
    min_float_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4,
        update=constrain_min_closure(float_4d_str),
    )
    max_float_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4, update=constrain_max_closure(float_4d_str)
    )

    # ---------------------
    # rgba
    rgba_4d_str = "rgba_4d"
    min_rgba_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4,
        update=constrain_rgba_closure("min_" + rgba_4d_str),  # noqa
    )
    max_rgba_4d: bpy.props.FloatVectorProperty(  # type: ignore
        size=4, update=constrain_rgba_closure("max_" + rgba_4d_str)  # noqa
    )

    # ---------------------
    # randomisation toggle
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# ------------------------------------
# ColSocketProperties
# ------------------------------------
def get_update_collection(self):
    """Get function for the update_collection attribute
    of the class ColSocketProperties

    It will run when the property value is 'get' and
    it will update the collection of socket properties if required

    Returns
    -------
    boolean
        returns True if the collection of socket properties is updated,
        otherwise it returns False
    """

    # set of sockets in collection
    set_of_sockets_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # set of sockets in graph
    set_of_sockets_in_graph = set(
        sck.node.name + "_" + sck.name
        for sck in bpy.context.scene.candidate_sockets
    )

    # set of sockets that are just in one of the two groups
    collection_needs_update = (
        set_of_sockets_in_collection_of_props.symmetric_difference(
            set_of_sockets_in_graph
        )
    )

    # if there is a difference:
    # overwrite the collection of sockets
    # with the latest data
    if collection_needs_update:
        set_update_collection(self, True)
        return True  # if returns True, it has been updated
    else:
        return False  # if returns False, it hasn't


def set_update_collection(self, value):
    """Set function for the update_collection attribute
    of the class ColSocketProperties.

    It will run when the property value is 'set'
    It will overwrite the collection of socket properties

    Parameters
    ----------
    value : boolean
        if True, the collection of socket properties is
        overwritten to consider the latest data
    """

    if value:
        # clear the collection of socket properties
        # TODO: remove() different elements
        # rather than clear() all?
        self.collection.clear()

        # overwrite the collection of socket properties
        # with the latest data
        for sckt in bpy.context.scene.candidate_sockets:
            sckt_prop = self.collection.add()
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


class ColSocketProperties(bpy.types.PropertyGroup):
    """Class holding the collection of socket properties and
    a boolean property to update the collection if required
    (for example, if new nodes are added)

    NOTE: we use the update_collection property as an
    auxiliary property because the CollectionProperty has no update function
    https://docs.blender.org/api/current/bpy.props.html#update-example

    """

    # collection of socket properties
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # 'dummy' attribute to update collection
    update_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_collection,
        set=set_update_collection,
    )


# ------------------------------------
# candidate_sockets prop
# ------------------------------------
def get_candidate_sockets(self):
    """Get function for the candidate_sockets property

    We define candidate sockets as the set of output sockets
    in input nodes, in the graph for the currently active
    material. Input nodes are nodes with only output sockets
    (i.e., no input sockets).

    It returns a list of sockets that are candidates for
    the randomisation.


    Returns
    -------
    list
        list of sockets in the input nodes in the graph
    """
    # list input nodes for current active material
    list_input_nodes = utils.get_material_input_nodes_to_randomise(
        bpy.context.object.active_material.name
    )

    # list of sockets
    # TODO: should we exclude unlinked ones here instead?
    list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
    return list_sockets


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
            bpy.types.Scene.sockets2randomise_props = bp.PointerProperty(
                type=ColSocketProperties
            )

    # link global Python variables to bpy.context.scene
    # if I use setattr: attribute must exist first right?
    for attr, attr_val in zip(
        ["socket_type_to_attr", "socket_type_to_ini_min_max"],
        [MAP_SOCKET_TYPE_TO_ATTR, MAP_SOCKET_TYPE_TO_INI_MIN_MAX],
    ):
        setattr(bpy.types.Scene, attr, attr_val)

    # Define candidate sockets as a Python managed property
    # 'bpy.context.scene.candidate_sockets' will provide an updated list of
    # candidate sockets
    bpy.types.Scene.candidate_sockets = property(fget=get_candidate_sockets)

    print("material properties registered")


def unregister():
    # unregister classes
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete the custom properties linked to bpy.context.scene
    list_attr = [
        "socket_type_to_attr",
        "socket_type_to_ini_min_max",
        "sockets2randomise_props",
        "candidate_sockets",
    ]
    for attr in list_attr:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    print("material properties unregistered")
