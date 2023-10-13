import re
from array import array

import bpy
import numpy as np

# -----------------------------------------------------------------
# Setter / getter methods for update_sockets_collection attribute
# ----------------------------------------------------------------


##### REFACTOR
def compute_UD_sockets_sets(self):
    """Compute the relevant sets of sockets for this specific
    user defined property, and add them to self.

    These sets include:
    - the set of sockets already in this GNG's collection
    - the set of sockets present in the Blender graph (for this GNG)
    - the set of sockets that are only in one of the two previous sets

    """

    # set of sockets in collection for this GNG
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )
    # pdb.set_trace()
    #####REFACTOR TO WORK WITH UI LIST/REMOVE
    # since don't need graphs for custom props?
    # set of sockets in graph for this GNG
    list_sckt_names_in_graph = [
        "UD_" + sck.name for sck in self.candidate_sockets
    ]
    self.set_sckt_names_in_graph = set(list_sckt_names_in_graph)

    # set of sockets that are just in one of the two groups
    self.set_of_sckt_names_in_one_only = (
        self.set_sckt_names_in_collection_of_props.symmetric_difference(
            self.set_sckt_names_in_graph
        )
    )


def get_update_collection(self):
    """Getter function for the update_sockets_collection attribute
    of the collection of socket properties class (ColSocketProperties)

    It will run when the property value is 'get' and
    it will update the collection of socket properties if required

    Returns
    -------
    boolean
        returns True if the collection of socket properties is updated,
        otherwise it returns False
    """
    # compute the different sets of sockets and add them to self
    compute_UD_sockets_sets(self)

    # if there is a difference between
    # sets of sockets in graph and in the collection:
    # edit the set of sockets in the collection
    if self.set_of_sckt_names_in_one_only:
        set_update_collection(self, True)
        return True
    else:
        return False


def set_update_collection(self, value):
    """
    Setter function for the update_sockets_collection attribute
    of the collection of socket properties class (ColSocketProperties)

    It will run when the property value is 'set'.

    It will update the collection of socket properties as follows:
        - For the set of sockets that exist only in either
        the collection or the graph:
            - if the socket exists only in the collection: remove from
            collection
            - if the socket exists only in the node graph: add to collection
            with initial values
        - For the rest of sockets: leave untouched

    Parameters
    ----------
    value : boolean
        if True, the collection of socket properties is
        overwritten to consider the latest data
    """

    #####REFACTOR TO WORK WITH UI LIST/REMOVE
    # since don't need graphs for custom props?
    if value:
        # if the update function is triggered directly and not via
        # the getter function: compute the sets here
        if not hasattr(self, "set_of_sckt_names_in_one_only"):
            compute_UD_sockets_sets(self)

        # update the sockets that are only in either
        # the collection set or the graph
        for sckt_name in self.set_of_sckt_names_in_one_only:
            # if the socket exists only in the collection: remove from
            # collection
            if sckt_name in self.set_sckt_names_in_collection_of_props:
                self.collection.remove(self.collection.find(sckt_name))

            # if the socket exists only in the node graph: add to collection
            # with initial values
            if sckt_name in self.set_sckt_names_in_graph:
                sckt_prop = self.collection.add()
                sckt_prop.name = sckt_name
                sckt_prop.bool_randomise = True

                # TODO: review - is this code block too hacky?
                # ---------------------------------------------
                # get socket object for this socket name
                # NOTE: my definition of socket name
                # (node.name + _ + socket.name)
                for s in self.candidate_sockets:
                    # build socket id from scratch
                    socket_id = "UD_" + s.name

                    if socket_id == sckt_name:
                        sckt = s
                        break

                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]

                # extract last number between '_' and 'd/D' in the
                # attribute name, to determine the shape of the array
                # TODO: there is probably a nicer way to do this...
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dictionary with initial min/max values
                # for this socket type
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
        # min_array.tolist()
        # max_array.tolist()
        print("MIN CLOSURE min_array ", type(min_array))
        print("MIN CLOSURE max_array ", type(max_array))

        print("MIN CLOSURE min_array FIRST", type(min_array[0]))
        print("MIN CLOSURE max_array FIRST", type(max_array[0]))
        if any(min_array > max_array):
            where_cond = np.where(min_array > max_array, max_array, min_array)
            print("np.where", where_cond)
            print("np.where type = ", type(where_cond))
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
        print("MAX CLOSURE min_array ", min_array)
        print("MAX CLOSURE max_array ", max_array)
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
            string specifying the socket attribute (e.g., int_1d)

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
            string specifying the socket attribute (e.g., int_1d)
        """
        # self is a 'SocketProperties' object
        # min_array = getattr(self, "min_" + m_str)
        # max_array = getattr(self, "max_" + m_str)
        min_array = np.array(getattr(self, "min_" + m_str))
        max_array = np.array(getattr(self, "max_" + m_str))

        # print("MIN CLOSURE min_array ", type(min_array))
        # MAX RECURSION DEPTH EXCEEDED WHILE CALLING A PYTHON OBJECT
        # print("MIN CLOSURE max_array ", type(max_array))

        # min_array = ast.literal_eval(str(min_array))
        # max_array = ast.literal_eval(str(max_array))
        # min_array = np.array(min_array)
        # max_array = np.array(max_array)

        # min_array = [pyt_int.item() for pyt_int in min_array]
        # max_array = [pyt_int.item() for pyt_int in max_array]

        # print("MIN CLOSURE min_array FIRST", type(min_array[0]))
        # print("MIN CLOSURE max_array FIRST", type(max_array[0]))

        # min_array = np.asarray(min_array,dtype="int")
        # max_array = np.asarray(max_array,dtype="int")
        min_array = array("i", min_array)
        max_array = array("i", max_array)
        # min_array = np.array(min_array)
        # max_array = np.array(max_array)

        # print("MIN CLOSURE min_array ", type(min_array))
        # print("MIN CLOSURE max_array ", type(max_array))

        # print("MIN CLOSURE min_array FIRST", type(min_array[0]))
        # print("MIN CLOSURE max_array FIRST", type(max_array[0]))
        # print(min_array > max_array)

        cond_min = [min > max for min, max in zip(min_array, max_array)]
        # if (min_array > max_array).all():
        if any(cond_min):
            cond = np.where(cond_min, max_array, min_array)
            print("np.where result = ", cond)
            print("np.where type = ", type(cond))

            setattr(
                self,
                "min_" + m_str,
                getattr(self, "max_" + m_str),
            )

            # try:
            #     setattr(
            #         self,
            #         "min_" + m_str,
            #         int(min_array[0]),
            #     )
            # except:
            #     print("int(min_array[0]) DID NOT WORK")

            # try:
            #     setattr(
            #         self,
            #         "min_" + m_str,
            #         getattr(self, "max_" + m_str),
            #     )
            # except:
            #     print('getattr(self, "min_" + m_str) DID NOT WORK')

        return

    return lambda slf, ctx: constrain_min(slf, ctx, m_str)


def constrain_max_closure_int(m_str):
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

    Because I think it is not possible to define attributes dynamically,
    for now we define an attribute for each possible socket type
    in the input nodes. These are all FloatVectors of different sizes.
    The size is specified in the attribute's name:
    - min/max_float_1d
    - min/max_float_3d
    - min/max_float_4d
    - min/max_rgba_4d

    """

    # TODO: how to set attributes dynamically?
    # TODO: I don't really get why this type definition is also an assignment?

    # # collection of socket properties for this GNG
    # collection: bpy.props.CollectionProperty()  # type: ignore

    # # helper attribute to update collection of socket properties
    # update_sockets_collection: bpy.props.BoolProperty(  # type: ignore
    #     default=False,
    #     get=get_update_collection,
    #     set=set_update_collection,
    # )

    # ---------------------
    # name of the socket
    # NOTE: if we make a Blender collection of this type of objects,
    # we will be able to access them by name
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
    # int_1d_str = "int_1d"
    # min_int_1d: bpy.props.IntVectorProperty(  # type: ignore
    #     size=1, update=constrain_min_closure(int_1d_str)
    # )

    # max_int_1d: bpy.props.IntVectorProperty(  # type: ignore
    #     size=1, update=constrain_max_closure(int_1d_str)
    # )
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
    # bool_1d_str = "bool_1d"
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
