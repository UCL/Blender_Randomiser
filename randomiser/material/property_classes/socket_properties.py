import bpy
import numpy as np


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
    min_int_1d: bpy.props.IntVectorProperty(  # type: ignore
        size=1, update=constrain_min_closure(int_1d_str)
    )

    max_int_1d: bpy.props.IntVectorProperty(  # type: ignore
        size=1, update=constrain_max_closure(int_1d_str)
    )

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
