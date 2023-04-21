import bpy
import numpy as np


# -----------------------------------------
# Bounds to PropertiesApplyRandomTransform
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
        # self is a 'PropertiesApplyRandomTransform' object
        min_array = np.array(getattr(self, m_str + "_min"))
        max_array = np.array(getattr(self, m_str + "_max"))
        if any(min_array > max_array):
            setattr(
                self,
                m_str + "_min",
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
        min_array = np.array(getattr(self, m_str + "_min"))
        max_array = np.array(getattr(self, m_str + "_max"))
        if any(max_array < min_array):
            setattr(
                self,
                m_str + "_max",
                np.where(max_array < min_array, min_array, max_array),
            )
        return

    return lambda slf, ctx: constrain_max(slf, ctx, m_str)


# ---------------------------
# Properties
class PropertiesApplyRandomTransform(bpy.types.PropertyGroup):
    # Camera position and rotation
    camera_pos: bpy.props.FloatVectorProperty(  # type: ignore
        size=3,
        step=100,
    )  # type: ignore
    camera_rot: bpy.props.FloatVectorProperty(  # type: ignore
        size=3,
        step=100,
    )  # type: ignore

    # Position min and max values
    camera_pos_x_str = "camera_pos_x"
    camera_pos_x_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_pos_x_str)
    )  # type: ignore
    camera_pos_x_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_pos_x_str)
    )  # type: ignore

    camera_pos_y_str = "camera_pos_y"
    camera_pos_y_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_pos_y_str)
    )  # type: ignore
    camera_pos_y_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_pos_y_str)
    )  # type: ignore

    camera_pos_z_str = "camera_pos_z"
    camera_pos_z_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_pos_z_str)
    )  # type: ignore
    camera_pos_z_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_pos_z_str)
    )  # type: ignore

    # Rotation min and max values
    camera_rot_x_str = "camera_rot_x"
    camera_rot_x_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_rot_x_str)
    )  # type: ignore
    camera_rot_x_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_rot_x_str)
    )  # type: ignore

    camera_rot_y_str = "camera_rot_y"
    camera_rot_y_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_rot_y_str)
    )  # type: ignore
    camera_rot_y_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_rot_y_str)
    )  # type: ignore

    camera_rot_z_str = "camera_rot_z"
    camera_rot_z_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_min_closure(camera_rot_z_str)
    )  # type: ignore
    camera_rot_z_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, step=100, update=constrain_max_closure(camera_rot_z_str)
    )  # type: ignore

    # BOOL
    bool_delta: bpy.props.BoolProperty()  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        if cls == PropertiesApplyRandomTransform:
            bpy.types.Scene.randomise_camera_props = bpy.props.PointerProperty(
                type=PropertiesApplyRandomTransform
            )

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.randomise_camera_props

    print("unregistered")