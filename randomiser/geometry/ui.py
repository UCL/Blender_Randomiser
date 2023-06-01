import bpy

from .. import config
from ..material.ui import TemplatePanel, draw_sockets_list


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomGeometryNodes(TemplatePanel):
    """Parent panel to the geometry node groups' subpanels

    Parameters
    ----------
    TemplatePanel : bpy.types.Panel
        base panel containing parts of the metadata common
        to all panels

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise GEOMETRY"

    @classmethod
    def poll(cls, context):
        """Determine whether the panel can be displayed.

        This panel is only displayed if there is an active object

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            True if there is an active object, False otherwise
        """
        return context.object is not None

    def draw(self, context):
        """Define the content to display in the main panel

        Parameters
        ----------
        context : _type_
            _description_
        """
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
    """Parent class for the geometry node groups' (GNG)
    subpanels

    Parameters
    ----------
    TemplatePanel : bpy.types.Panel
        base panel containing parts of the metadata common
        to all panels

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "NODE_GEOMETRY_PT_subpanel"
    bl_parent_id = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"DEFAULT_CLOSED"}
    # NOTE: other bl_options in the link below
    # https://docs.blender.org/api/master/bpy.types.Panel.html#bpy.types.Panel.bl_options

    @classmethod
    def poll(cls, context):
        """Determine whether the GNG subpanel can be displayed.

        To display a subpanels, its index must be lower than the
        total number of GNGs defined in the scene

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        cs = context.scene

        # force an update on the group nodes collection first
        if cs.socket_props_per_gng.update_gngs_collection:
            print("Collection of Geometry Node Groups updated")

        return cls.subpanel_gng_idx < len(cs.socket_props_per_gng.collection)

    def draw_header(self, context):
        """Define header for the GNG subpanel

        The header shows the name of the associated geometry node group
        (GNG) inside a button. The button is linked to the view-graph
        operator.

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's GNG
        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]

        # add view graph operator to layout
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.operator(
            f"node.view_graph_for_gng_{self.subpanel_gng_idx}",
            text=subpanel_gng.name,
            emboss=True,
        )

    def draw(self, context):
        """Define the content to display in the GNG subpanel

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's GNG
        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]

        # force an update in the sockets for this GNG
        if cs.socket_props_per_gng.collection[
            subpanel_gng.name
        ].update_sockets_collection:
            print("Collection of Geometry Node Groups updated")

        # get (updated) collection of socket props for this GNG
        sockets_props_collection = cs.socket_props_per_gng.collection[
            subpanel_gng.name
        ].collection

        # Get list of input nodes to randomise for this subpanel's GNG
        list_parent_nodes_str = [
            sckt.name.split("_")[0] for sckt in sockets_props_collection
        ]

        list_input_nodes = [
            bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
            for nd_str in list_parent_nodes_str
        ]

        # Draw sockets to randomise per input node, including their
        # current value and min/max boundaries
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
    """Panel containing the 'randomise-all' button

    Parameters
    ----------
    TemplatePanel : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "NODE_GEOMETRY_PT_subpanel_operator"
    bl_parent_id = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        """Determine whether the panel can be displayed.

        This panel is only displayed if there is an active object

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            True if there is an active object, False otherwise
        """
        return context.object is not None

    def draw(self, context):
        """Define the content to display in the
        randomise-all operator panel

        Parameters
        ----------
        context : _type_
            _description_
        """
        column = self.layout.column(align=True)
        column.operator(
            "node.randomise_all_geometry_sockets",
            text="Randomise",
        )


# -----------------------
# Classes to register
# ---------------------

# add Main panel to the list of classes to register
list_classes_to_register = [
    MainPanelRandomGeometryNodes,
]

# Define (dynamically) a subpanel class for each Geometry Node Group (GNGs)
# and add them to the list of classes to register
# NOTE: because we don't know the number of GNGs that will be
# defined a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is lower than the total number of GNGs defined in the scene.
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    # define subpanel class for GNG i
    subpanel_class_i = type(
        f"NODE_GEOMETRY_PT_subpanel_{i}",
        (SubPanelRandomGeometryNodes,),
        {
            "bl_idname": f"NODE_GEOMETRY_PT_subpanel_{i}",
            "subpanel_gng_idx": i,
        },
    )
    # append to list of classes to register
    list_classes_to_register.append(subpanel_class_i)  # type: ignore


# add Subpanel with operator to the list
# NOTE: to render it as the last panel
# we add it as the last one to the list
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
