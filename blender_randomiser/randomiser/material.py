"""
An add-on to randomise the material parameters
of the selected objects

"""
### Imports
import re

import bpy
import numpy as np
from bpy.app.handlers import persistent

from . import utils

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
# Bounds to input values
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


# -------------------------------
## Operators
class RandomiseMaterialNodes(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise the selected output sockets

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # operator metadata
    bl_idname = "node.randomise_socket"  # this is appended to bpy.ops.
    bl_label = "Randomise selected sockets from input material nodes"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current (object) context
    # NOTE: but it actually checks if there is an object in this context right?
    @classmethod
    def poll(cls, context):
        return context.object is not None

    # ------------------------------

    def invoke(self, context, event):
        """Initialise parmeters before executing

        The invoke() function runs before executing the operator.
        Here, we
        - add the list of input nodes and collection of socket propertiess to
          the operator self,
        - unselect the randomisation toggle of the sockets of input nodes if
          they are not linked to any other node

        Parameters
        ----------
        context : bpy_types.Context
            the context from which the operator is executed
        event : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        # add list of input nodes to operator self
        self.list_input_nodes = utils.get_material_input_nodes_to_randomise()

        # add list of socket properties to operator self
        # OJO I think the collection is populated once, with load_post!
        # --------------
        self.sockets_props_collection = context.scene.sockets2randomise_props

        # -----------
        # can I add elements to the collection here?
        # ....
        # -----------

        # if socket unlinked and toggle is true: set toggle to false
        for nd in self.list_input_nodes:
            for out in nd.outputs:
                sckt_id = nd.name + "_" + out.name
                if (not out.is_linked) and (
                    self.sockets_props_collection[sckt_id].bool_randomise
                ):
                    setattr(
                        self.sockets_props_collection[sckt_id],
                        "bool_randomise",
                        False,
                    )

        return self.execute(context)

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        """Execute the randomiser operator

        Randomise the selected output sockets between
        the min/max values provided

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        # Construct a numpy random number generator
        rng = np.random.default_rng()

        # Loop thru input nodes and their selected output sockets
        # to assign to each a uniformly sampled value btw min and max
        for nd in self.list_input_nodes:
            # get list of selected sockets for this node
            list_sockets_to_randomise = [
                sck
                for sck in nd.outputs
                if (
                    self.sockets_props_collection[
                        nd.name + "_" + sck.name
                    ].bool_randomise
                )
            ]

            # randomise their value
            for out in list_sockets_to_randomise:
                socket_id = nd.name + "_" + out.name

                # min value for this socket
                min_val = np.array(
                    getattr(
                        self.sockets_props_collection[socket_id],
                        "min_" + context.scene.socket_type_to_attr[type(out)],
                    )
                )

                # max value for this socket
                max_val = np.array(
                    getattr(
                        self.sockets_props_collection[socket_id],
                        "max_" + context.scene.socket_type_to_attr[type(out)],
                    )
                )

                # if type of the socket is color, and max_val < min_val:
                # switch them before randomising
                # NOTE: these are not switched in the display panel
                # (this is intended)
                if (type(out) == bpy.types.NodeSocketColor) and any(
                    max_val < min_val
                ):
                    max_val_new = np.where(
                        max_val >= min_val, max_val, min_val
                    )
                    min_val_new = np.where(min_val < max_val, min_val, max_val)

                    # TODO: is there a more elegant way?
                    # feels a bit clunky....
                    max_val = max_val_new
                    min_val = min_val_new

                # assign randomised socket value between min and max
                out.default_value = rng.uniform(low=min_val, high=max_val)

        return {"FINISHED"}


# -------
# Panel
class PanelRandomMaterialNodes(bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_random"
    bl_label = "Randomise material nodes"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        # TODO: is the object context what I need to check?
        return context.object is not None

    def draw(self, context):
        # Get list of input nodes to randomise
        list_input_nodes = utils.get_material_input_nodes_to_randomise()

        # get collection of sockets' properties
        sockets_props_collection = context.scene.sockets2randomise_props

        # define UI fields for every socket property
        layout = self.layout
        for i_n, nd in enumerate(list_input_nodes):
            row = layout.row()

            # if first node: add labels for
            # name, min, max and randomisation toggle
            if i_n == 0:
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                # input node name
                col1.label(text=nd.name)
                col1.alignment = "CENTER"

                # min label
                col3.alignment = "CENTER"
                col3.label(text="min")

                # max label
                col4.alignment = "CENTER"
                col4.label(text="max")

            # if not first node: add just node name
            else:
                row.label(text=nd.name)

            # add sockets for this node in the subseq rows
            for i_o, out in enumerate(nd.outputs):
                # split row in 5 columns
                row = layout.row()
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                # socket name
                col1.alignment = "RIGHT"
                col1.label(text=out.name)

                # socket current value
                col2.prop(
                    out,
                    "default_value",
                    icon_only=True,
                )
                col2.enabled = False  # (not editable)

                # socket min and max columns
                socket_id = nd.name + "_" + out.name
                for m_str, col in zip(["min", "max"], [col3, col4]):
                    # if color socket: format as a color wheel
                    if type(out) == bpy.types.NodeSocketColor:
                        # show color property via color picker
                        # ATT! It doesn't include alpha!
                        col.template_color_picker(
                            sockets_props_collection[socket_id],
                            m_str
                            + "_"
                            + context.scene.socket_type_to_attr[
                                type(out)
                            ],  # property
                        )
                        # show color property as an array too (including alpha)
                        for j, cl in enumerate(["R", "G", "B", "alpha"]):
                            col.prop(
                                sockets_props_collection[socket_id],
                                m_str
                                + "_"
                                + context.scene.socket_type_to_attr[
                                    type(out)
                                ],  # property
                                icon_only=False,
                                text=cl,
                                index=j,
                                # ATT! if I pass -1 it will use all
                                # elements of the array (rather than
                                # the last one)
                            )
                    # if not color socket: format as a regular prop
                    else:
                        col.prop(
                            sockets_props_collection[socket_id],
                            m_str
                            + "_"
                            + context.scene.socket_type_to_attr[
                                type(out)
                            ],  # property
                            icon_only=True,
                        )

                # randomisation toggle
                col5.prop(
                    sockets_props_collection[socket_id],
                    "bool_randomise",
                    icon_only=True,
                )

        # add Randomise button
        row = layout.row(align=True)
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)
        col5 = row_split.column(align=True)
        col5.alignment = "LEFT"
        col5.operator("node.randomise_socket", text="Randomise")


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelRandomMaterialNodes,
    RandomiseMaterialNodes,
    SocketProperties,
]


# -------------------------------------
# Add elements to the collection of socket properties
# About the @persistent decorator
# - If I don't label it as 'persistent', it will get removed from the
#   bpy.app.handlers.load_pre list after the fn is run for the first time
# - Because I add it to the bpy.app.handlers.load_pre list, it will only
#   be executed when a new file is open
# I need to run this before the draw() function of the panel!
# TODO: is there another way to do this without relying on handlers?
@persistent
def initialise_collection_of_socket_properties(dummy):
    # not sure why I need dummy here?

    # get list of input nodes
    list_input_nodes = utils.get_material_input_nodes_to_randomise()

    # instantiate collection
    sockets_props_collection = bpy.context.scene.sockets2randomise_props

    # add elements to the collection of socket properties
    # (one per output socket)
    for nd in list_input_nodes:
        for out in nd.outputs:
            # add a socket to the collection
            sckt = sockets_props_collection.add()

            # add socket name
            sckt.name = nd.name + "_" + out.name

            # add randomising checkbox
            sckt.bool_randomise = True

            # ---------------------------
            # add min/max values
            # TODO: review - is this too hacky?
            # for this socket type, get the name of the attribute
            # holding the min/max properties
            socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                type(out)
            ]
            # for the shape of the array from the attribute name:
            # extract last number between '_' and 'd/D' in the attribute name
            n_dim = int(re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1])
            # ---------------------------

            # get dict with initial min/max values for this socket type
            ini_min_max_values = bpy.context.scene.socket_type_to_ini_min_max[
                type(out)
            ]

            # assign
            for m_str in ["min", "max"]:
                setattr(
                    sckt,
                    m_str + "_" + socket_attrib_str,
                    (ini_min_max_values[m_str],) * n_dim,
                )

    return


def register():
    """
    This is run when the add-on is enabled
    """

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # add the collection of socket properties
        # to bpy.context.scene
        if cls == SocketProperties:
            bp = bpy.props
            bpy.types.Scene.sockets2randomise_props = bp.CollectionProperty(
                type=SocketProperties  # type of the elements in the collection
            )

    # global Python variables
    setattr(bpy.types.Scene, "socket_type_to_attr", MAP_SOCKET_TYPE_TO_ATTR)
    setattr(
        bpy.types.Scene,
        "socket_type_to_ini_min_max",
        MAP_SOCKET_TYPE_TO_INI_MIN_MAX,
    )

    # add fn w/ list of sockets creation to load_post
    # TODO: is there a better way? is load_pre better?
    # can I define a custom handler?
    # TODO: an alternative may be to use invoke() or check() functions
    # in a dummy operator?
    bpy.app.handlers.load_post.append(
        initialise_collection_of_socket_properties
    )

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete global Python vars
    delattr(bpy.types.Scene, "socket_type_to_attr")
    delattr(bpy.types.Scene, "socket_type_to_ini_min_max")

    # remove aux fn from handlers
    bpy.app.handlers.load_post.remove(
        initialise_collection_of_socket_properties
    )

    # delete the custom property
    del bpy.types.Scene.sockets2randomise_props
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="sockets2randomise_props"
    )

    print("unregistered")
