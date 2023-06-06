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
class PropertiesCustomTransform(bpy.types.PropertyGroup):
    """
    Class holding the set of properties
    for the camera position and rotation:
    - min/max values for x/y/z component of position and rotation, and
    - boolean for delta position and rotation
    - boolean for setting seed value
    - integer for the actual seed value

    """

    # Position min and max values
    custom_input_prop = bpy.props.StringProperty(name="enter text")
    custom_input: custom_input_prop  # type: ignore
    custom_min: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,  # update=constrain_min_closure(custom_input)
    )  # type: ignore
    custom_max: bpy.props.FloatVectorProperty(  # type: ignore
        size=1,
        step=100,  # update=constrain_max_closure(custom_input)
    )  # type: ignore
    custom_idx: bpy.props.IntProperty(default=0)  # type: ignore

    # BOOL
    bool_rand_cust: bpy.props.BoolProperty(default=True)  # type: ignore


class PropertiesCustomList(bpy.types.PropertyGroup):
    custom_string_prop = bpy.props.StringProperty(default="camera.location")
    custom_string: custom_string_prop  # type: ignore


custom_string_prop = bpy.props.StringProperty(default="camera.location")


class CUSTOM_colorCollection(bpy.types.PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    id_prop = bpy.props.IntProperty()
    id: id_prop  # type: ignore


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesCustomTransform,
    PropertiesCustomList,
    CUSTOM_colorCollection,
]

list_context_scene_attr = ["socket_type_to_attr"]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        if cls == PropertiesCustomTransform:
            bpy.types.Scene.custom_props = bpy.props.PointerProperty(
                type=PropertiesCustomTransform
            )

        if cls == PropertiesCustomList:
            bpy.types.Scene.custom_list = bpy.props.PointerProperty(
                type=PropertiesCustomList
            )

        for attr, attr_val in zip(
            list_context_scene_attr,
            [custom_string_prop],
        ):
            setattr(bpy.types.Scene, attr, attr_val)

        # Custom scene properties
        if cls == CUSTOM_colorCollection:
            bpy.types.Scene.custom = bpy.props.CollectionProperty(
                type=CUSTOM_colorCollection
            )
        bpy.types.Scene.custom_index = bpy.props.IntProperty()
    print("transform properties registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.custom_props
    del bpy.types.Scene.custom_list

    # delete the custom properties linked to bpy.context.scene
    for attr in list_context_scene_attr:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

    print("transform properties unregistered")
