import bpy

from .. import config

# from .. import utils
from ..material.ui import TemplatePanel, draw_sockets_list


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomGeometryNodes(TemplatePanel):
    bl_idname = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise GEOMETRY"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        column = self.layout.column(align=True)
        column.label(
            text=(
                "Click on a node group to display its graph "
                "on the Geometry Node Editor"
            )
        )


# ------------------------------
# Subpanel for each node group
# -----------------------------
class SubPanelRandomGeometryNodes(TemplatePanel):
    bl_idname = "NODE_GEOMETRY_PT_subpanel"
    bl_parent_id = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"DEFAULT_CLOSED"}
    # https://docs.blender.org/api/master/bpy.types.Panel.html#bpy.types.Panel.bl_options

    @classmethod
    def poll(cls, context):
        cs = context.scene

        # force an update on the group nodes collection first
        # the '.update_collection' attribute
        # triggers the get function that checks if an update is
        # required. If it is, the collection of sockets is updated
        # and returns TRUE
        if cs.socket_props_per_gng.update_gngs_collection:
            print("Collection of Geometry Node Groups updated")

        # only display subpanels for which this is true
        return cls.subpanel_gng_idx < len(cs.socket_props_per_gng.collection)

    def draw_header(self, context):
        cs = context.scene

        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # For now: view graph button on top of material name
        layout.label(text=subpanel_gng.name)
        # layout.operator(
        #     f"node.view_graph_for_material_{self.subpanel_material_idx}",
        #     text=subpanel_gng.name,
        #     emboss=True,
        # )

    def draw(self, context):
        # name of the GNG for this panel
        cs = context.scene
        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]

        # force an update in the sockets for this GNG
        if cs.socket_props_per_gng.collection[
            subpanel_gng.name
        ].update_sockets_collection:
            print("Collection of Geometry Node Groups updated")

        # get collection of socket props for this GNG
        sockets_props_collection = cs.socket_props_per_gng.collection[
            subpanel_gng.name
        ].collection

        # Get list of input nodes to randomise
        # for this subpanel's GNG
        # list_input_nodes = utils.get_geometry_nodes_to_randomise(
        # subpanel_gng.name
        # ) #this does not exclude strings!--these should be the nodes with
        list_parent_nodes_str = [
            sckt.name.split("_")[0] for sckt in sockets_props_collection
        ]

        list_input_nodes = [
            bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
            for nd_str in list_parent_nodes_str
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
class SubPanelRandomGeometryOperator(TemplatePanel):
    bl_idname = "NODE_GEOMETRY_PT_subpanel_operator"
    bl_parent_id = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            "node.randomise_all_geometry_sockets",
            text="Randomise",
        )


# -----------------------
# Classes to register
# ---------------------

# Main panel
list_classes_to_register = [
    MainPanelRandomGeometryNodes,
]

# Subpanel for each node group
# Define a subpanel class for each Geometry Node Group (GNGs)
# (defined dynamically)
# NOTE: because we don't know the number of GNGs that will be
# defiend a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is < len(list_of_materials).
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    # define subpanel class for GNG i
    subpanel_class_i = type(
        f"NODE_GEOMETRY_PT_subpanel_{i}",
        (
            SubPanelRandomGeometryNodes,
            # bpy.types.Panel,
        ),  # parent classes (Q FOR REVIEW: is Panel req?)
        {
            "bl_idname": f"NODE_GEOMETRY_PT_subpanel_{i}",
            "subpanel_gng_idx": i,
        },
    )
    # append to list of classes to register
    list_classes_to_register.append(subpanel_class_i)  # type: ignore


# Subpanel with operator
# NOTE: we need to add it as the last one to the list,
# to render it at the bottom
list_classes_to_register.append(SubPanelRandomGeometryOperator)


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("geometry UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("geometry UI unregistered")
