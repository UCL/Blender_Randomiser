import bpy

from .. import utils


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


class CUSTOM_UL_items(bpy.types.UIList):
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


class MainPanelRandomCustomProps(TemplatePanel, bpy.types.Panel):
    """Class defining the panel for randomising
    the camera transform

    """

    bl_idname = "CUSTOM_PROPS_PT_mainpanel"
    bl_label = "Randomise CUSTOM PROPS"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.label(
            text="Choose property to see available properties to randomise"
        )
        column.prop(context.scene.custom_props, "custom_input", text="")
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
    print(list_input_nodes_sorted)
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

            col1.label(text=nd.name)
            col2.label(text="")
            col3.label(text="min")
            col4.label(text="max")
            col5.label(text="index")

            # # input node name
            # col1.label(text=nd.name)
            # col1.alignment = "CENTER"

            # # min label
            # col3.alignment = "CENTER"
            # col3.label(text="min")

            # # max label
            # col4.alignment = "CENTER"
            # col4.label(text="max")

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

    # def draw(self, context):

    #     col1.prop(context.scene.custom_props, "custom_input", text="")
    #     # col1.enabled = False

    #     # col1.label(context.scene.custom_props, "custom_input")
    #     # col1.enabled=True

    #     col2.prop(
    #         context.scene.custom_props,
    #         "custom_min",
    #         icon_only=True,
    #     )

    #     col3.prop(
    #         context.scene.custom_props,
    #         "custom_max",
    #         icon_only=True,
    #     )

    #     col4.prop(
    #         context.scene.custom_props,
    #         "custom_idx",
    #         icon_only=True,
    #     )

    #     col5.prop(
    #         context.scene.custom_props,
    #         "bool_rand_cust",
    #         icon_only=True,
    #     )

    #     # Bool delta
    #     col = self.layout.column()

    #     # Randomise button
    #     col.operator("opr.apply_random_custom_prop", text="Randomise")


# ------------------------------
# Subpanel for each material
# -----------------------------
class SubPanelRandomCustomProps(TemplatePanel, bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    bl_idname = "CUSTOM_PROPS_PT_subpanel"
    bl_parent_id = "CUSTOM_PROPS_PT_mainpanel"
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
        if cs.socket_props_per_material.get_update_collection:
            print("Collection of materials updated")

        # only display subpanels for which this is true
        return cls.subpanel_custom_idx < len(
            cs.socket_props_per_material.collection
        )

    def draw_header(self, context):
        cs = context.scene
        # TODO: maybe a dict? can order of materials change?
        cs.socket_props_per_material.collection[self.subpanel_custom_idx]

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # # For now: view graph button on top of material name
        # layout.operator(
        #     f"node.view_graph_for_material_{self.subpanel_custom_idx}",
        #     text=subpanel_custom.name,
        #     emboss=True,
        # )

    def draw(self, context):
        # get name of the material for this subpanel
        cs = context.scene
        subpanel_custom = cs.socket_props_per_material.collection[
            self.subpanel_custom_idx
        ]

        # then force an update in the sockets per material
        # subpanel_material_name = subpanel_material.name
        if cs.socket_props_per_material.collection[
            subpanel_custom.name
        ].update_sockets_collection:
            print("Collection of sockets updated")

        # get (updated) collection of socket properties
        # for the current material
        sockets_props_collection = cs.socket_props_per_material.collection[
            subpanel_custom.name
        ].collection

        # Get list of input nodes to randomise
        # for this subpanel's material
        list_input_nodes = utils.get_custom_props_to_randomise_indep(
            subpanel_custom.name
        )

        draw_sockets_list(
            cs,
            self.layout,
            list_input_nodes,
            sockets_props_collection,
        )


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    MainPanelRandomCustomProps,
    CUSTOM_UL_items,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("custom UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("custom UI unregistered")
