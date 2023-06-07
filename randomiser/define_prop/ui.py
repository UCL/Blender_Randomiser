import bpy

from ..material.ui import TemplatePanel  # draw_sockets_list


# ---------------------------------------------------
# Custom UIlist items
# ----------------------------------------------------
class CUSTOM_UL_items(bpy.types.UIList):
    print("hello UIlist")

    def draw_item(
        self,
        context,
        layout,
        data,
        item,
        icon,
        active_data,
        active_propname,
        index,
    ):
        split = layout.split(factor=0.3)
        split.label(text="Index: %d" % (index))
        custom_icon = "COLOR"
        split.prop(item, "name", icon=custom_icon, emboss=False, text="")

    def invoke(self, context, event):
        pass


# ---------------------------------------------------
# Common layout for list of sockets to randomise
# ----------------------------------------------------
##### REFACTOR to removed list input nodes
def draw_sockets_list_UD(
    cs,
    layout,
    list_input_nodes,
    sockets_props_collection,
):
    # Define UI fields for every socket property
    # NOTE: if I don't sort the input nodes, everytime one of the nodes is
    # selected in the graph it moves to the bottom of the panel.
    list_input_nodes_sorted = sorted(list_input_nodes, key=lambda x: x.name)
    print(list_input_nodes_sorted)
    for i_n, nd in enumerate(list_input_nodes_sorted):
        row = layout.row()

        # if first node: add labels for
        # name, min, max and randomisation toggle
        if i_n == 0:
            row_split = row.split()
            col1 = row_split.column(align=True)
            row_split.column(align=True)
            col3 = row_split.column(align=True)
            col4 = row_split.column(align=True)
            row_split.column(align=True)

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
        # for sckt in nd.outputs:
        #     # split row in 5 columns
        #     row = layout.row()
        #     row_split = row.split()
        #     col1 = row_split.column(align=True)
        #     col2 = row_split.column(align=True)
        #     col3 = row_split.column(align=True)
        #     col4 = row_split.column(align=True)
        #     col5 = row_split.column(align=True)

        #     # socket name
        #     col1.alignment = "RIGHT"
        #     col1.label(text=sckt.name)

        #     # socket current value
        #     col2.prop(
        #         sckt,
        #         "default_value",
        #         icon_only=True,
        #     )
        #     col2.enabled = False  # current value is not editable

        #     # socket min and max columns
        #     socket_id = nd.name + "_" + sckt.name
        #     if (nd.id_data.name in bpy.data.node_groups) and (
        #         bpy.data.node_groups[nd.id_data.name].type != "GEOMETRY"
        #     ):  # only for SHADER groups
        #         socket_id = nd.id_data.name + "_" + socket_id

        #     # if socket is a color: format min/max as a color picker
        #     # and an array (color picker doesn't include alpha value)
        #     if type(sckt) == bpy.types.NodeSocketColor:
        #         for m_str, col in zip(["min", "max"], [col3, col4]):
        #             # color picker
        #             col.template_color_picker(
        #                 sockets_props_collection[socket_id],
        #                 m_str + "_" + cs.socket_type_to_attr[type(sckt)],
        #             )
        #             # array
        #             for j, cl in enumerate(["R", "G", "B", "alpha"]):
        #                 col.prop(
        #                     sockets_props_collection[socket_id],
        #                     m_str + "_" + cs.socket_type_to_attr[type(sckt)],
        #                     icon_only=False,
        #                     text=cl,
        #                     index=j,
        #                 )
        #     # if socket is Boolean: add non-editable labels
        #     elif type(sckt) == bpy.types.NodeSocketBool:
        #         for m_str, col in zip(["min", "max"], [col3, col4]):
        #             m_val = getattr(
        #                 sockets_props_collection[socket_id],
        #                 m_str + "_" + cs.socket_type_to_attr[type(sckt)],
        #             )
        #             col.label(text=str(list(m_val)[0]))

        #     # if socket is not color type: format as a regular property
        #     else:
        #         for m_str, col in zip(["min", "max"], [col3, col4]):
        #             col.prop(
        #                 sockets_props_collection[socket_id],
        #                 m_str + "_" + cs.socket_type_to_attr[type(sckt)],
        #                 icon_only=True,
        #             )

        #     # randomisation toggle
        #     col5.prop(
        #         sockets_props_collection[socket_id],
        #         "bool_randomise",
        #         icon_only=True,
        #     )


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomUD(
    TemplatePanel
):  # MainPanelRandomGeometryNodes(TemplatePanel):
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

    bl_idname = "UD_PROPS_PT_mainpanel"  # "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise UD"  # "Randomise GEOMETRY"

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
        column.label(text=("Add properties to randomise"))


class SubPanelUDUIlist(TemplatePanel):
    """Panel containing the UI list

    Parameters
    ----------
    TemplatePanel : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "UD_PT_subpanel_UIlist"
    bl_parent_id = "UD_PROPS_PT_mainpanel"
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
        column = self.layout.column(align=True)
        column.label(
            text="Choose property to see available properties to randomise"
        )
        # column.prop(context.scene.custom_props, "custom_input", text="")
        # column.operator("opr.add_custom_prop_to_list",
        # text="Add to Custom List")

        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = self.layout.row()
        row.template_list(
            "CUSTOM_UL_items",
            "",
            scn,
            "custom",
            scn,
            "custom_index",
            rows=rows,
        )

        col = row.column(align=True)
        col.operator(
            "custom.list_action", icon="ZOOM_IN", text=""
        ).action = "ADD"
        col.operator(
            "custom.list_action", icon="ZOOM_OUT", text=""
        ).action = "REMOVE"
        col.separator()
        col.operator(
            "custom.list_action", icon="TRIA_UP", text=""
        ).action = "UP"
        col.operator(
            "custom.list_action", icon="TRIA_DOWN", text=""
        ).action = "DOWN"

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator(
            "custom.print_items", icon="LINENUMBERS_ON"
        )  # LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")


# ------------------------------
# Subpanel for each node group
# -----------------------------
class SubPanelRandomUD(
    TemplatePanel
):  # SubPanelRandomGeometryNodes(TemplatePanel):
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

    bl_idname = "UD_PROPS_PT_subpanel"
    bl_parent_id = "UD_PROPS_PT_mainpanel"
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
        if cs.socket_props_per_UD.update_gngs_collection:
            print("Collection of Geometry Node Groups updated")
            ######pointer needs defined in collection_UD_sock_props?
            # In redundant materials level (only need sockets)

        return cls.subpanel_gng_idx < len(
            cs.socket_props_per_UD.collection
        )  #####clc.subpanel defined in operators.py
        # only display subpanels for which this is true
        # return cls.subpanel_custom_idx < len(
        #     cs.socket_props_per_material.collection
        # )

    def draw_header(
        self, context
    ):  # maybe needed for the name of custom props
        # but no need graph to be displayed
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
        subpanel_gng = cs.socket_props_per_UD.collection[self.subpanel_gng_idx]

        # add view graph operator to layout
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.operator(
            f"node.view_graph_for_gng_{self.subpanel_gng_idx}",
            text=subpanel_gng.name,
            emboss=True,
        )  #####operator defined once node.view_graph_for_gng
        # - not needed for custom props?

    def draw(self, context):
        """Define the content to display in the GNG subpanel

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's GNG
        subpanel_gng = cs.socket_props_per_UD.collection[self.subpanel_gng_idx]
        #####NEED TO COMBINE THESE TWO PARTS INTO JUST SOCKETS
        # force an update in the sockets for this GNG
        if cs.socket_props_per_UD.collection[
            subpanel_gng.name
        ].update_sockets_collection:
            print("Collection of Geometry Node Groups updated")

        # get (updated) collection of socket props for this GNG
        sockets_props_collection = cs.socket_props_per_UD.collection[
            subpanel_gng.name
        ].collection

        # Get list of input nodes to randomise for this subpanel's GNG
        list_parent_nodes_str = [
            sckt.name.split("_")[0] for sckt in sockets_props_collection
        ]
        #####REMOVE INPUT NODES FROM SOCKETS LIST FOR CUSTOM PROPS
        list_input_nodes = [
            bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
            for nd_str in list_parent_nodes_str
        ]

        # Draw sockets to randomise per input node, including their
        # current value and min/max boundaries
        draw_sockets_list_UD(
            cs,
            self.layout,
            list_input_nodes,  ##### remove once refactored
            sockets_props_collection,
        )


# -------------------------------------------
# Subpanel for the 'randomise-all' operator
# -------------------------------------------
class SubPanelRandomUDOperator(
    TemplatePanel
):  # SubPanelRandomGeometryOperator(TemplatePanel): #RANDOMISATION
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

    bl_idname = (
        "UD_PT_subpanel_operator"  # "NODE_GEOMETRY_PT_subpanel_operator"
    )
    bl_parent_id = "UD_PROPS_PT_mainpanel"  # "NODE_GEOMETRY_PT_mainpanel"
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
            "opr.randomise_all_ud_sockets",
            text="Randomise",
        )


# -----------------------
# Classes to register
# ---------------------

# add Main panel to the list of classes to register
list_classes_to_register = [
    MainPanelRandomUD,
    CUSTOM_UL_items,
]

# Define (dynamically) a subpanel class for each Geometry Node Group (GNGs)
# and add them to the list of classes to register
# NOTE: because we don't know the number of GNGs that will be
# defined a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is lower than the total number of GNGs defined in the scene.
# for i in range(config.MAX_NUMBER_OF_SUBPANELS):
#     # define subpanel class for GNG i
#     # subpanel_class_i = type(
#     #     f"NODE_GEOMETRY_PT_subpanel_{i}",
#     #     (SubPanelRandomGeometryNodes,),
#     #     {
#     #         "bl_idname": f"NODE_GEOMETRY_PT_subpanel_{i}",
#     #         "subpanel_gng_idx": i,
#     #     },
#     # )
#     subpanel_class_i = type(
#         f"UD_PT_subpanel_{i}",
#         (SubPanelRandomUD,),
#         {
#             "bl_idname": f"UD_PT_subpanel_{i}",
#             "subpanel_gng_idx": i,  ##### IN UI AND OPERATORS
#         },
#     )

#     # append to list of classes to register
#     list_classes_to_register.append(subpanel_class_i)  # type: ignore


# add Subpanel with operator to the list
# NOTE: to render it as the last panel
# we add it as the last one to the list
list_classes_to_register.append(SubPanelUDUIlist)
list_classes_to_register.append(SubPanelRandomUDOperator)


#     SubPanelRandomUDOperator,
#     SubPanelUDUIlist
# )


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("UD props UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("UD props UI unregistered")
