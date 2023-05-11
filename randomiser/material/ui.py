"""
Solution to show all materials in subpanels inspired on this SO answer:
https://blender.stackexchange.com/questions/185693/how-can-i-control-the-number-of-sub-panel-instances-from-an-intproperty

"""
import bpy

from .. import utils
from . import config


# ----------------------
# Common sections
# ---------------------
class TemplatePanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"  # this shows up as the tab name


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomMaterialNodes(TemplatePanel, bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_mainpanel"
    bl_label = "Randomise MATERIAL"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.label(text="Select material to see available sockets.")


# ------------------------------
# Subpanel for each material
# -----------------------------
class SubPanelRandomMaterialNodes(TemplatePanel, bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    bl_idname = "NODE_MATERIAL_PT_subpanel"
    bl_parent_id = "NODE_MATERIAL_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    # bl_options = {"DEFAULT_CLOSED"}
    # https://docs.blender.org/api/master/bpy.types.Panel.html#bpy.types.Panel.bl_options

    @classmethod
    def poll(cls, context):
        cs = context.scene

        # force an update on the materials collection first
        # the '.update_collection' attribute
        # triggers the get function that checks if an update is
        # required. If it is, the collection of sockets is updated
        # and returns TRUE
        if cs.socket_props_per_material.update_materials_collection:
            print("Collection of materials updated")

        # only display subpanels for which this is true
        return cls.subpanel_material_idx < len(
            cs.socket_props_per_material.collection
        )

    def draw_header(self, context):
        cs = context.scene
        # TODO: maybe a dict? can order of materials change?
        subpanel_material = cs.socket_props_per_material.collection[
            self.subpanel_material_idx
        ]

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # For now: view graph button on top of material name
        layout.operator(
            f"node.view_graph_for_material_{self.subpanel_material_idx}",
            text=subpanel_material.name,
            emboss=True,
        )

    def draw(self, context):
        # get name of the material for this subpanel
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.collection[
            self.subpanel_material_idx
        ]

        # Get list of input nodes to randomise
        # for this subpanel's material
        list_input_nodes = utils.get_material_input_nodes_to_randomise(
            subpanel_material.name
        )

        # then force an update in the sockets per material
        # subpanel_material_name = subpanel_material.name
        if cs.socket_props_per_material.collection[
            subpanel_material.name
        ].update_sockets_collection:
            print("Collection of sockets updated")

        # get (updated) collection of socket properties
        # for the current material
        sockets_props_collection = cs.socket_props_per_material.collection[
            subpanel_material.name
        ].collection

        # Define UI fields for every socket property
        # NOTE: if I don't sort the input nodes, everytime one of the nodes is
        # selected in the graph it moves to the bottom of the panel.
        # TODO: sort by date of creation instead?
        # ---I didn't find an easy way to do this
        layout = self.layout
        for i_n, nd in enumerate(
            sorted(
                list_input_nodes,
                key=lambda x: x.name
                if x.id_data.name not in bpy.data.node_groups
                else x.id_data.name + "_" + x.name,
            )
        ):
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
                node_label = nd.name
                if nd.id_data.name in bpy.data.node_groups:
                    node_label = nd.id_data.name + "_" + node_label
                col1.label(text=node_label)
                col1.alignment = "CENTER"

                # min label
                col3.alignment = "CENTER"
                col3.label(text="min")

                # max label
                col4.alignment = "CENTER"
                col4.label(text="max")

            # if not first node: add just node name
            else:
                row.separator(factor=1.0)  # add empty row before each node
                row = layout.row()

                node_label = nd.name
                if nd.id_data.name in bpy.data.node_groups:
                    node_label = nd.id_data.name + "_" + node_label
                row.label(text=node_label)

            # add sockets for this node in the subseq rows
            for sckt in nd.outputs:
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
                col1.label(text=sckt.name)

                # socket current value
                col2.prop(
                    sckt,
                    "default_value",
                    icon_only=True,
                )
                col2.enabled = False  # current value is not editable

                # socket min and max columns
                socket_id = nd.name + "_" + sckt.name
                if nd.id_data.name in bpy.data.node_groups:
                    socket_id = nd.id_data.name + "_" + socket_id

                # for m_str, col in zip(["min", "max"], [col3, col4]):
                # if socket is a color: format min/max as a color picker
                # and an array (color picker doesn't include alpha value)
                if type(sckt) == bpy.types.NodeSocketColor:
                    for m_str, col in zip(["min", "max"], [col3, col4]):
                        # color picker
                        col.template_color_picker(
                            sockets_props_collection[socket_id],
                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                        )
                        # array
                        for j, cl in enumerate(["R", "G", "B", "alpha"]):
                            col.prop(
                                sockets_props_collection[socket_id],
                                m_str
                                + "_"
                                + cs.socket_type_to_attr[type(sckt)],
                                icon_only=False,
                                text=cl,
                                index=j,
                            )
                # if socket is not color type: format as a regular property
                else:
                    for m_str, col in zip(["min", "max"], [col3, col4]):
                        col.prop(
                            sockets_props_collection[socket_id],
                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                            icon_only=True,
                        )

                # randomisation toggle
                col5.prop(
                    sockets_props_collection[socket_id],
                    "bool_randomise",
                    icon_only=True,
                )


# -----------------------------------
# Subpanel for randomise-all operator
# ----------------------------------
class SubPanelRandomMaterialOperator(TemplatePanel, bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_subpanel_operator"
    bl_parent_id = "NODE_MATERIAL_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            "node.randomise_all_sockets",
            text="Randomise",
        )


# -----------------------
# Classes to register
# ---------------------

# main panel
list_classes_to_register = [
    MainPanelRandomMaterialNodes,
]

# subpanels per material (defined dynamically)
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    subpanel_class_i = type(
        f"NODE_MATERIAL_PT_subpanel_{i}",
        (
            SubPanelRandomMaterialNodes,
            bpy.types.Panel,
        ),  # parent classes (Q FOR REVIEW: is Panel req?)
        {
            "bl_idname": f"NODE_MATERIAL_PT_subpanel_{i}",
            "subpanel_material_idx": i,
        },
    )
    list_classes_to_register.append(subpanel_class_i)  # type: ignore

# subpanel with operator
# (add the last one to the list,
# render it at the bottom)
list_classes_to_register.append(SubPanelRandomMaterialOperator)


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("material UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material UI unregistered")
