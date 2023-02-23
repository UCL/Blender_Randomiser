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


class PropertiesMaterialNodes(bpy.types.PropertyGroup):
    node_str: bpy.props.StringProperty()  # type: ignore
    # int_value_min_max: bpy.props.IntVectorProperty(name="Int value",
    #   default=(0,0,0))
    # float_value_min_max: bpy.props.FloatVectorProperty(name="Float value",
    #   default=(0.0,0.0,0.0))

    min_value: bpy.props.FloatProperty(default=0)  # type: ignore
    max_value: bpy.props.FloatProperty(default=0)  # type: ignore


#


# -------------------------------
## Operators
class RandomiseMaterialNodes(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Add a random cube within a predefined volume"""

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
    # takes list of nodes, min and max from properties and
    # changes default value
    def execute(self, context):
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

    def draw(self, context):
        list_input_nodes = [
            no
            for no in bpy.data.materials[
                "Material"
            ].node_tree.nodes  # ----bpy.data cannot be accessed here
            if len(no.inputs) == 0 and no.name.lower().startswith("random")
        ]

        layout = self.layout
        # co=0 # TODO: improve this counter approach
        for i_n, nd in enumerate(list_input_nodes):
            # node
            row = layout.row()

            if i_n == 0:
                # row.label(text=nd.name)
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                col1.label(text=nd.name)
                col3.alignment = "CENTER"
                # ‘EXPAND’, ‘LEFT’, ‘CENTER’, ‘RIGHT’ (I dont find differences
                # btw the first 3)
                col3.label(text="min")
                col4.alignment = "CENTER"
                col4.label(text="max")
            else:
                row.label(text=nd.name)

            # node output sockets
            for i_o, out in enumerate(nd.outputs):
                row = layout.row()
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                col1.alignment = "RIGHT"
                col1.label(text=out.name)

                # prop = out.bl_rna.properties['default_value']
                col2.prop(
                    out, "default_value", icon_only=True
                )  # col2.prop(prop,'default',icon_only=True)
                col3.prop(
                    context.scene.material_custom_params[i_o],
                    "min_value",
                    icon_only=True,
                )
                col4.prop(
                    context.scene.material_custom_params[i_o],
                    "max_value",
                    icon_only=True,
                )

                col5.operator("node.randomise_socket", text="Randomize")

                # co += 1

                # https://blender.stackexchange.com/questions/165056/how-to-get-the-max-and-min-value-of-a-certain-nodesockets-slider
                #  bpy.data.materials['Material'].node_tree.nodes[2].outputs[0].bl_rna.properties['default_value'].type
                # 'FLOAT'
                #  bpy.data.materials['Material'].node_tree.nodes[2].outputs[0].bl_rna.properties['default_value'].unit

                # if out.type == 'VALUE': # maybe check type(out) instead?
                #     col2.prop(out,'default_value',icon_only=True)
                #     col3.prop(context.scene,f'{nd.name}_{out.name}_max')
                #     col4.prop(context.scene,f'{nd.name}_{out.name}_min')


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelRandomMaterialNodes,
    RandomiseMaterialNodes,
    PropertiesMaterialNodes,
]


@persistent
def add_properties_per_node_output(scene):
    print("PATATA")

    list_input_nodes_str = [
        nd
        for nd in bpy.data.materials[
            "Material"
        ].node_tree.nodes  # ----bpy.data cannot be accessed here
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random")
    ]

    # add elements of the collection--one per output
    for nd in list_input_nodes_str:
        for out in nd.outputs:
            p = (
                bpy.context.scene.material_custom_params.add()
            )  # add an element to the collection
            p.node_str = out.name
            p.min_value = out.default_value * 10
            p.max_value = out.default_value / 10


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
        if cls == PropertiesMaterialNodes:
            # ---do I need to make it a pointer?
            # bpy.types.Scene.material_custom_params =
            # bpy.props.PointerProperty(
            #     type=PropertiesMaterialNodes
            # )
            # ---do I need to make it a pointer?
            typ_scene = bpy.types.Scene
            typ_scene.material_custom_params = bpy.props.CollectionProperty(
                type=PropertiesMaterialNodes  # elements of the collection
            )
            # bpy.context.scene.collection_node_outputs ---> will be a
            # collection of properties

    bpy.app.handlers.load_post.append(add_properties_per_node_output)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete the custom property pointer
    # NOTE: this is different from its accessor, as that is a read/write only
    # to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.material_custom_params  # ------How?

    bpy.app.handlers.load_post.remove(add_properties_per_node_output)

    print("unregistered")
