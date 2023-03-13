"""
An add-on to randomise the material parameters
of the selected objects

"""
### Imports
import re

import bpy
import numpy as np
from bpy.app.handlers import persistent

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

# TODO: eventually add option to read
# initial, min and max values from config file?
INITIAL_MIN_MAX_FLOAT = [-np.inf, np.inf]  # should be float
INITIAL_MIN_MAX_RGBA = [1.0, 1.0]
# for color, rather than min/max these are maybe extremes in a colormap?


# -----------------------------------------
# Bounds to input values
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


def constrain_rgba(self, context, min_or_max_full_str):
    # self is a 'SocketProperties' object
    # if min > max --> min is reset to max value
    # (i.e., no randomisation)
    min_or_max_array = np.array(getattr(self, min_or_max_full_str))
    if any(min_or_max_array > 1.0) or any(min_or_max_array < 0.0):
        setattr(
            self,
            min_or_max_full_str,
            np.clip(min_or_max_array, 0.0, 1.0),
        )
    return


def constrain_min_closure(m_str):
    return lambda slf, ctx: constrain_min(slf, ctx, m_str)


def constrain_max_closure(m_str):
    return lambda slf, ctx: constrain_max(slf, ctx, m_str)


def constrain_rgba_closure(m_str):
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

    name: bpy.props.StringProperty()  # type: ignore

    # float properties: they default to 0s
    # ---------------------
    ### float 1d
    float_1d_str = "float_1d"
    min_float_1d: bpy.props.FloatVectorProperty(  # type: ignore
        size=1, update=constrain_min_closure(float_1d_str)
    )
    # Q for review: is this better for the update fn?
    # (more prone to error?)
    # update = lambda slf, ctx: constrain_max(slf, ctx, 'float_1d')?
    # I need to check this min/max agreement before numpy
    # TODO: setting attributes dynamically..
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
## Operators --dummy operator for now
class RandomiseMaterialNodes(bpy.types.Operator):
    # docstring will show as a tooltip for menu items and buttons.
    """Randomise 'RandomMetallic' default value"""

    # operator metadata
    bl_idname = "node.randomise_socket"  # this is appended to bpy.ops.
    bl_label = "Randomise input node's output socket"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current context
    @classmethod
    def poll(cls, context):
        return context.object is not None

    # ------------------------------
    ### Invoke: runs before execute
    # - add list of input nodes and list of socket props to self
    # - unselect output sockets in input nodes if they are unlinked
    def invoke(self, context, event):
        # get list of nodes
        self.list_input_nodes = [
            no
            for no in bpy.data.materials["Material"].node_tree.nodes
            if len(no.inputs) == 0 and no.name.lower().startswith("random")
        ]

        # get list of socket properties
        self.sockets_props_collection = context.scene.sockets2randomise_props

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
        # set the output sockets with checkbox=True
        # to a random value

        # construct a generator
        rng = np.random.default_rng()

        # loop thru input nodes and
        # selected output sockets
        # to assign uniformly sampled value btw min and max
        for nd in self.list_input_nodes:
            list_sockets_to_randomise = [
                sck
                for sck in nd.outputs
                if (
                    self.sockets_props_collection[
                        nd.name + "_" + sck.name
                    ].bool_randomise
                )
            ]

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
                # switch them
                # Note that color sockets do not have an 'update' fn
                # but numpy does not accept max_val < min_val
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

                # set socket value
                out.default_value = rng.uniform(low=min_val, high=max_val)

        return {"FINISHED"}


# -------
# Panel
class PanelRandomMaterialNodes(bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_random"
    bl_label = "Randomise MATERIAL"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        # TODO: is the object context what I need to check?
        return context.object is not None

    def draw(self, context):
        # Get list of input nodes that start with 'random'
        # input nodes are those that have no input sockets
        # (i.e., only output sockets)
        list_input_nodes = [
            no
            for no in bpy.data.materials["Material"].node_tree.nodes
            if len(no.inputs) == 0 and no.name.lower().startswith("random")
        ]

        # for every input node and every output socket
        layout = self.layout
        # get collection of sockets' properties
        sockets_props_collection = context.scene.sockets2randomise_props
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

                col1.label(text=nd.name)
                col1.alignment = "CENTER"

                col3.alignment = "CENTER"
                col3.label(text="min")

                col4.alignment = "CENTER"
                col4.label(text="max")

            # if not first node: add just node name
            else:
                row.label(text=nd.name)

            # add sockets for this node in the subseq rows
            for i_o, out in enumerate(nd.outputs):
                socket_id = nd.name + "_" + out.name

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
                # if color, format as a color wheel
                if type(out) == bpy.types.NodeSocketColor:
                    for m, col in zip(["min", "max"], [col3, col4]):
                        # color picker
                        # ATT! It doesn't include alpha!
                        col.template_color_picker(
                            sockets_props_collection[socket_id],
                            m
                            + "_"
                            + context.scene.socket_type_to_attr[
                                type(out)
                            ],  # property
                        )
                        # color as an array too (including alpha)
                        # TODO: maybe only alpha?
                        # the max value allowed is not v intuitive...
                        for j, cl in enumerate(["R", "G", "B", "alpha"]):
                            col.prop(
                                sockets_props_collection[socket_id],
                                m
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
                else:
                    for m, col in zip(["min", "max"], [col3, col4]):
                        col.prop(
                            sockets_props_collection[socket_id],
                            m
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
def add_properties_per_socket(dummy):
    # not sure why I need dummy here?

    # get list of input nodes
    list_input_nodes = [
        nd
        for nd in bpy.data.materials["Material"].node_tree.nodes
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random")
    ]

    # add elements to the collection of socket properties
    # (one per output socket)
    sockets_props_collection = bpy.context.scene.sockets2randomise_props
    for nd in list_input_nodes:
        for out in nd.outputs:
            # add a socket to the collection
            sckt = sockets_props_collection.add()
            sckt.name = nd.name + "_" + out.name
            sckt.bool_randomise = True

            # assign min/max initial values
            # TODO: eventually add option to read
            # initial, min and max values from config file?
            socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                type(out)
            ]
            # for the shape of the array:
            # extract last number between '_' and 'd/D' in the attribute name
            n_dim = int(re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1])
            # TODO: is this too hacky?
            if type(out) == bpy.types.NodeSocketColor:
                for m, m_val in zip(
                    ["min", "max"],
                    INITIAL_MIN_MAX_RGBA,
                ):
                    setattr(
                        sckt,
                        m + "_" + socket_attrib_str,
                        (m_val,) * n_dim,
                    )  # if I use this for color wheel it's still fine

            else:
                for m, m_val in zip(
                    ["min", "max"],
                    INITIAL_MIN_MAX_FLOAT,
                ):
                    setattr(
                        sckt,
                        m + "_" + socket_attrib_str,
                        (m_val,) * n_dim,
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

    # add fn w/ list of sockets creation to load_post
    # TODO: is there a better way? is load_pre better?
    # can I define a custom handler?
    # TODO: an alternative may be to use invoke() or check() functions
    # in a dummy operator?
    bpy.app.handlers.load_post.append(add_properties_per_socket)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete global Python vars
    delattr(bpy.types.Scene, "socket_type_to_attr")

    # remove aux fn from handlers
    bpy.app.handlers.load_post.remove(add_properties_per_socket)

    # delete the custom property
    del bpy.types.Scene.sockets2randomise_props
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="sockets2randomise_props"
    )

    print("unregistered")
