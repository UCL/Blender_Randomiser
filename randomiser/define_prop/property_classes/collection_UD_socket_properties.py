import re
from array import array

import bpy
import numpy as np

# -----------------------------------------------------------------
# Setter / getter methods for update_sockets_collection attribute
# ----------------------------------------------------------------


def compute_UD_sockets_sets(self):
    """Compute the relevant sets of UD props and add them to self.

    These sets include:
    - the set of UD props already in the UD props collection
    - the set of UD props present in the candidate sockets
    - the set of UD props that are only in one of the two previous sets

    """

    # set of UD props in collection for this GNG
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # should be renamed candidate UD props
    list_sckt_names_in_graph = [
        "UD_" + sck.name for sck in self.candidate_sockets
    ]
    self.set_sckt_names_in_graph = set(list_sckt_names_in_graph)

    # set of UD props that are just in one of the two groups
    self.set_of_sckt_names_in_one_only = (
        self.set_sckt_names_in_collection_of_props.symmetric_difference(
            self.set_sckt_names_in_graph
        )
    )


def get_update_collection(self):
    """Getter function for the update_sockets_collection attribute
    of the collection of UD properties class (SocketProperties)

    It will run when the property value is 'get' and
    it will update the collection of UD properties if required

    Returns
    -------
    boolean
        returns True if the collection of UD properties is updated,
        otherwise it returns False
    """
    # compute the different sets of UD props and add them to self
    compute_UD_sockets_sets(self)

    # if there is a difference between
    # sets of UD props in graph and in the collection:
    # edit the set of UD props in the collection
    if self.set_of_sckt_names_in_one_only:
        set_update_collection(self, True)
        return True
    else:
        return False


def set_update_collection(self, value):
    """
    Setter function for the update_sockets_collection attribute
    of the collection of UD properties class (SocketProperties)

    It will run when the property value is 'set'.

    It will update the collection of UD properties as follows:
        - For the set of UD props that exist only in either
        the collection or the graph:
            - if the UD prop exists only in the collection: remove from
            collection
            - if the UD propexists only in the node graph: add to collection
            with initial values
        - For the rest of sockets: leave untouched

    Parameters
    ----------
    value : boolean
        if True, the collection of UDproperties is
        overwritten to consider the latest data
    """

    if value:
        # if the update function is triggered directly and not via
        # the getter function: compute the sets here
        if not hasattr(self, "set_of_sckt_names_in_one_only"):
            compute_UD_sockets_sets(self)

        # update the UD props that are only in either
        # the collection set or the graph
        for sckt_name in self.set_of_sckt_names_in_one_only:
            # if the UD prop exists only in the collection: remove from
            # collection
            if sckt_name in self.set_sckt_names_in_collection_of_props:
                self.collection.remove(self.collection.find(sckt_name))

            # if the UD prop exists only in the node graph: add to collection
            # with initial values
            if sckt_name in self.set_sckt_names_in_graph:
                sckt_prop = self.collection.add()
                sckt_prop.name = sckt_name
                sckt_prop.bool_randomise = True

                # ---------------------------------------------
                # get UD prop object for this UD prop name
                for s in self.candidate_sockets:
                    # build UD prop id from scratch
                    socket_id = "UD_" + s.name

                    if socket_id == sckt_name:
                        sckt = s
                        break

                # for this UD prop type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]

                # extract last number between '_' and 'd/D' in the
                # attribute name, to determine the shape of the array
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dictionary with initial min/max values
                # for this UD props type
                ini_min_max_values = (
                    bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                )

                # assign initial value
                for m_str in ["min", "max"]:
                    setattr(
                        sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )


# -----------------------------------------
# Bounds to SocketProperties
# -----------------------------------------


def constrain_min_closure(m_str):
    """Constain min value with closure

    Parameters
    ----------
    m_str : str
            string specifying the UD propattribute (e.g., float_1d)

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
            string specifying the UD propattribute (e.g., float_1d)
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
        string specifying the UD propattribute (e.g., float_1d)

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
            string specifying the UD propattribute (e.g., float_1d)
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


def constrain_min_closure_int(m_str):
    """Constain min value with closure

    Parameters
    ----------
    m_str : str
            string specifying the UD propattribute (e.g., int_1d)

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
            string specifying the UD propattribute (e.g., int_1d)
        """
        # self is a 'SocketProperties' object
        min_array = np.array(getattr(self, "min_" + m_str))
        max_array = np.array(getattr(self, "max_" + m_str))

        min_array = array("i", min_array)
        max_array = array("i", max_array)

        cond_min = [min > max for min, max in zip(min_array, max_array)]
        if any(cond_min):
            setattr(
                self,
                "min_" + m_str,
                getattr(self, "max_" + m_str),
            )

        return

    return lambda slf, ctx: constrain_min(slf, ctx, m_str)


def constrain_max_closure_int(m_str):
    """Constain max value with closure

    Parameters
    ----------
    m_str : str
        string specifying the UD propattribute (e.g., float_1d)

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
            string specifying the UD propattribute (e.g., float_1d)
        """
        # self is a 'SocketProperties' object
        min_array = np.array(getattr(self, "min_" + m_str))
        max_array = np.array(getattr(self, "max_" + m_str))

        cond_max = [max < min for max, min in zip(max_array, min_array)]
        if any(cond_max):
            setattr(
                self,
                "max_" + m_str,
                getattr(self, "min_" + m_str),
            )
        return

    return lambda slf, ctx: constrain_max(slf, ctx, m_str)


def constrain_rgba_closure(m_str):
    """Constain RGBA value with closure

    Parameters
    ----------
    m_str : str
        string specifying the UD propattribute (e.g., float_1d)

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
            string specifying the UD propattribute (e.g., float_1d)
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
    - UD propname,
    - min/max values, and
    - boolean for randomisation

    Because I think it is not possible to define attributes dynamically,
    for now we define an attribute for each possible UD proptype
    in the input nodes. These are all FloatVectors of different sizes.
    The size is specified in the attribute's name:
    - min/max_float_1d
    - min/max_float_3d
    - min/max_float_4d
    - min/max_rgba_4d

    """

    # ---------------------
    # name of the socket
    # NOTE: if we make a Blender collection of this type of objects,
    # we will be able to access them by name
    name: bpy.props.StringProperty()  # type: ignore

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

    euler_str = "euler"
    min_euler: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_min_closure(euler_str)
    )
    max_euler: bpy.props.FloatVectorProperty(  # type: ignore
        update=constrain_max_closure(euler_str)
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

    # ----------------------------
    # int_1d
    int_1d_str = "int_1d"
    min_int_1d_PROP = bpy.props.IntVectorProperty(  # type: ignore
        size=1, update=constrain_min_closure_int(int_1d_str)
    )
    min_int_1d: min_int_1d_PROP  # type: ignore

    max_int_1d_PROP = bpy.props.IntVectorProperty(  # type: ignore
        size=1, update=constrain_max_closure_int(int_1d_str)
    )
    max_int_1d: max_int_1d_PROP  # type: ignore

    # ----------------------------
    # bool_1d
    min_bool_1d: bpy.props.BoolVectorProperty(  # type: ignore
        size=1,
    )

    max_bool_1d: bpy.props.BoolVectorProperty(  # type: ignore
        size=1,
    )

    # ---------------------
    # randomisation toggle
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# Register / unregister
def register():
    bpy.utils.register_class(SocketProperties)


def unregister():
    bpy.utils.unregister_class(SocketProperties)
