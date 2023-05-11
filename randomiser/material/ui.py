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


# ---------------------------------------------------
# Common layout for list of sockets to randomise
# ----------------------------------------------------
def draw_sockets_list(
    cs,
    layout,
    list_input_nodes,
    sockets_props_collection,
):
    # Define UI fields for every socket property
    # NOTE: if I don't sort the input nodes, everytime one of the nodes is
    # selected in the graph it moves to the bottom of the panel.
    list_input_nodes_sorted = sorted(list_input_nodes, key=lambda x: x.name)
    for i_n, nd in enumerate(list_input_nodes_sorted):
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
            row.separator(factor=1.0)  # add empty row before each node
            row = layout.row()

            row.label(text=nd.name)

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
                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
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

        # Get list of input nodes to randomise
        # for this subpanel's material
        list_input_nodes = utils.get_material_nodes_to_randomise_indep(
            subpanel_material.name
        )

        draw_sockets_list(
            cs,
            self.layout,
            list_input_nodes,
            sockets_props_collection,
        )


# -----------------------------------
# Subsubpanel for node groups
# ----------------------------------
class SubSubPanelGroupNodes(TemplatePanel, bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    bl_idname = "NODE_MATERIAL_PT_subsubpanel"
    bl_parent_id = "NODE_MATERIAL_PT_subpanel"  # use bl_idname
    bl_label = ""
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        # force an update on the materials collection first
        # the '.update_collection' attribute
        # triggers the get function that checks if an update is
        # required. If it is, the collection of sockets is updated
        # and returns TRUE
        # TODO: is this required here? (I am already updating when the parent
        # subpanel is drawn)
        cs = context.scene
        if cs.socket_props_per_material.update_materials_collection:
            print("Collection of materials updated")

        # get material of parent subpanel and add to class
        cls.subpanel_material_str = cs.socket_props_per_material.collection[
            cls.subpanel_material_idx  # can I access this here?
        ].name

        # get list of *group nodes names* for this material and add to class
        # exclude groups with no nodes to randomise inside!
        # TODO: is it better to add to cls somewhere else? (not sure where...)
        cls.list_nodes2rand_in_groups = (
            utils.get_material_nodes_to_randomise_group(
                cls.subpanel_material_str
            )
        )

        # list of group nodes names with nodes to randomise
        # (only show group nodes in panel if they have nodes to randomise)
        list_group_nodes_names_this_material = sorted(
            list(set([k.id_data.name for k in cls.list_nodes2rand_in_groups]))
        )

        # add group node name to subsubpanel class
        if cls.subsubpanel_group_node_idx < len(
            list_group_nodes_names_this_material
        ):
            cls.group_node_name = list_group_nodes_names_this_material[
                cls.subsubpanel_group_node_idx
            ]
        # else:
        #     cls.group_node_name = '' # not needed

        # only display this sub-subpanel if its index is < total group nodes
        # for this material
        return cls.subsubpanel_group_node_idx < len(
            list_group_nodes_names_this_material
        )

    def draw_header(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # show name of the group node
        layout.label(text=self.group_node_name)

    def draw(self, context):
        # get name of the material for this subpanel
        cs = context.scene

        # then force an update in the sockets per material
        # TODO: do I need this? it should update when drawing the subpanel
        if cs.socket_props_per_material.collection[
            self.subpanel_material_str
        ].update_sockets_collection:
            print("Collection of sockets updated")

        # get (updated) collection of socket properties
        # for the current material
        sockets_props_collection = cs.socket_props_per_material.collection[
            self.subpanel_material_str
        ].collection

        # Get list of input nodes to randomise
        # for this subpanel's material
        # only nodes inside groups!
        # keep only nodes inside this group!
        list_input_nodes = [
            nd
            for nd in self.list_nodes2rand_in_groups
            if nd.id_data.name == self.group_node_name
        ]

        draw_sockets_list(
            cs,
            self.layout,
            list_input_nodes,
            sockets_props_collection,
        )


# -------------------------------------------
# Subpanel for the 'randomise-all' operator
# -------------------------------------------
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

# Main panel
list_classes_to_register = [
    MainPanelRandomMaterialNodes,
]

# Subpanels per material, and subsubpanels per group node.
# Define a subpanel class for each material (defined dynamically)
# NOTE: because we don't know the number of materials that will be
# defiend a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is < len(list_of_materials). We apply the same startegy
# for the subsubpanels
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    # define subpanel class for material i
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
    # append to list of classes to register
    list_classes_to_register.append(subpanel_class_i)  # type: ignore

    # define n=MAX_NUMBER_OF_SUBSUBPANELS subsubpanel classes
    # for each material i
    for k in range(config.MAX_NUMBER_OF_SUBSUBPANELS):
        subsubpanel_class_k = type(
            f"NODE_MATERIAL_PT_subpanel_{i}_subsubpanel_{k}",
            (
                SubSubPanelGroupNodes,
                bpy.types.Panel,
            ),
            {
                "bl_idname": f"NODE_MATERIAL_PT_subsubpanel_{i}_{k}",
                "bl_parent_id": f"NODE_MATERIAL_PT_subpanel_{i}",
                "subpanel_material_idx": i,
                "subsubpanel_group_node_idx": k,
            },
        )

        # append to list of classes to register
        list_classes_to_register.append(subsubpanel_class_k)  # type: ignore

# Subpanel with operator
# NOTE: we need to add it as the last one to the list,
# to render it at the bottom
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
