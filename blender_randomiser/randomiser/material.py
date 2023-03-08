"""
An add-on to randomise the material parameters
of the selected objects

"""
### Imports
import bpy
import numpy as np
from bpy.app.handlers import persistent

# -------------------
# Type of node
# bpy.data.materials['Material'].node_tree.nodes[0].outputs[0].bl_idname

# Type of output socket? (float)
# https://docs.blender.org/api/current/bpy.types.NodeSocket.html#bpy.types.NodeSocket.type


# ----------------------------
## Properties
# for every node:
# - make a dict with key=node_str and values: min/max value to randomise, and
#   randomize toggle?
# for every node:
# - make a property that is a list of all node_str?
# - make a property for each min/max value? (initialise with soft max/min?
#   same type as the value? (so that they are rendered the same way?))
# - follow this?: https://blender.stackexchange.com/questions/127409/how-do-i-pass-an-argument-to-an-operator-that-is-called-inside-a-panel


# ---------------------
# Python global vars
# TODO: can I combine these?
# TODO: use out.type=='VALUE', 'RGBA' instead? (type of the output socket)
# TODO: rethink this mapping....
# https://docs.blender.org/api/current/bpy.types.NodeSocket.html#bpy.types.NodeSocket.type
# the idea is to map nodesocket types to property types I can use in the UI
# Types of properties:
#  bpy.props.
#           BoolProperty(
#           BoolVectorProperty(
#           CollectionProperty(
#           EnumProperty(
#           FloatProperty(
#           FloatVectorProperty(
#           IntProperty(
#           IntVectorProperty(
#           PointerProperty(
#           RemoveProperty(
#           StringProperty(

MAP_SOCKET_TYPE_TO_BPY_PROP = {
    bpy.types.NodeSocketFloat: "float_1d",
    bpy.types.NodeSocketColor: "int_4d",
}


# NodeSocket types:
# https://docs.blender.org/api/current/bpy.types.html
# - bool
# - collection
# - color
# - float
# - float angle (why not simply float?)
# - float distance (why not simply float?)
# - float/int factor
# - float/int percentage
# - float time
# - float unsigned
# - int


# -----------------------
# Blender global variables (is that the right way to think about it?)
class Socket(bpy.types.PropertyGroup):
    """
    Properties for a socket element

    Types of properties:---I think these relate to UI buttons
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

    # int props: defaults to 0s
    min_int_1d: bpy.props.IntVectorProperty(size=1)  # type: ignore
    max_int_1d: bpy.props.IntVectorProperty(size=1)  # type: ignore

    min_int_4d: bpy.props.IntVectorProperty(size=4)  # type: ignore
    max_int_4d: bpy.props.IntVectorProperty(size=4)  # type: ignore

    # float props: defaults to 0s
    min_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore
    max_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore

    min_float_3d: bpy.props.FloatVectorProperty()  # type: ignore
    max_float_3d: bpy.props.FloatVectorProperty()  # type: ignore

    # BOOL
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# -------------------------------
## Operators
class RandomiseMaterialNodes(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise 'RandomMetallic' default value"""

    # operator metadata
    bl_idname = "node.randomise_socket"  # appended to bpy.ops.
    bl_label = "Randomise input node's output socket"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current context
    @classmethod
    def poll(cls, context):
        return context.object is not None

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        # pass
        rng = np.random.default_rng()
        node_tree = bpy.data.materials["Material"].node_tree
        node_tree.nodes["RandomMetallic"].outputs[0].default_value = (
            100 * rng.random()
        )

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
        return context.object is not None
        # TODO: is the object context what I need to check?

    def draw(self, context):
        # list of input nodes that start with 'random'
        # input nodes are those that have no input sockets
        list_input_nodes = [
            no
            for no in bpy.data.materials["Material"].node_tree.nodes
            if len(no.inputs) == 0 and no.name.lower().startswith("random")
        ]

        # for every input node and every output socket
        co = 0  # TODO: improve this counter approach---get sockets by name?
        layout = self.layout
        # get collection of sockets' properties
        sockets_props_collection = context.scene.sockets2randomise
        for i_n, nd in enumerate(list_input_nodes):
            row = layout.row()

            # if first node: add labels for name, min, max and
            # randomise toggle
            if i_n == 0:
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                col1.label(text=nd.name)
                col3.alignment = "CENTER"
                # ‘EXPAND’, ‘LEFT’, ‘CENTER’, ‘RIGHT’
                # (I dont see differences btw the first 3?)
                col3.label(text="min")
                col4.alignment = "CENTER"
                col4.label(text="max")

            # else, add just node name
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
                # (not editable)
                col2.prop(
                    out,
                    "default_value",
                    icon_only=True,
                )
                col2.enabled = False

                # socket min and max columns
                # TODO: is out.type better as a key to the dict?
                for m, col in zip(["min", "max"], [col3, col4]):
                    col.prop(
                        sockets_props_collection[
                            sockets_props_collection.find(socket_id)
                        ],
                        m
                        + "_"
                        + context.scene.socket2prop_type[
                            type(out)
                        ],  # property
                        icon_only=True,
                    )

                # randomisation toggle
                col5.prop(
                    sockets_props_collection[
                        sockets_props_collection.find(socket_id)
                    ],
                    "bool_randomise",
                    icon_only=True,
                )

                co += 1

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
    Socket,
]


# -------------------------------------
# Add sockets to scene property
# About the @persistent decorator
# - If I don't label it as 'persistent', it will get removed from the
#   bpy.app.handlers.load_pre list after the fn is run for the first time
# - Because I add it to the bpy.app.handlers.load_pre list, it will only
#   be executed when a new file is open (is there a better way for this?)
@persistent
def add_properties_per_socket(dummy):  # not sure why I need dummy here?
    sockets_props_collection = bpy.context.scene.sockets2randomise
    print("here")
    print(len(sockets_props_collection))

    # get list of input nodes
    list_input_nodes = [
        nd
        for nd in bpy.data.materials["Material"].node_tree.nodes
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random")
    ]

    # add elements to the collection of socket properties
    # (one per output socket)
    for nd in list_input_nodes:
        print(nd.name)
        for out in nd.outputs:
            # add a socket to the collection
            sckt = sockets_props_collection.add()
            sckt.name = nd.name + "_" + out.name
            sckt.bool_randomise = True

            # ---------------------------------
            if type(out) == bpy.types.NodeSocketFloat:  # out.type=='VALUE':
                sckt.min_float_1d = (-np.inf,)  # -------setattr?
                sckt.max_float_1d = (np.inf,)
            elif type(out) == bpy.types.NodeSocketColor:  # out.type=='RGBA':
                sckt.min_int_4d = (1, 2, 333, 4)
                sckt.max_int_4d = (10, 20, 3000, 40)
            # ---------------------------------
    print(len(sockets_props_collection))

    return


def register():
    """
    This is run when the add-on is enabled
    """

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

        # for the property class: add it to bpy.context.scene
        # TODO: do I need to make it a pointer?
        if cls == Socket:
            bpy.types.Scene.sockets2randomise = bpy.props.CollectionProperty(
                type=Socket  # specify type of the elements in the collection
            )

    # global Python var
    setattr(bpy.types.Scene, "socket2prop_type", MAP_SOCKET_TYPE_TO_BPY_PROP)

    # add fn w/ list of sockets creation to load_post
    # TODO: is there a better way? is load_pre better?
    # can I define a custom handler?
    bpy.app.handlers.load_post.append(add_properties_per_socket)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # global Python vars?
    delattr(bpy.types.Scene, "socket2prop_type")

    # remove aux fn from handlers
    bpy.app.handlers.load_post.remove(add_properties_per_socket)

    # delete the custom property pointer
    # NOTE: this is different from its accessor, as that is a read/write only
    # to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.sockets2randomise  # ------How?
    bpy.ops.wm.properties_remove(
        data_path="scene", property_name="sockets2randomise"
    )

    print("unregistered")
