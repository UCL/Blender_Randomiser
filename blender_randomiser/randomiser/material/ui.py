import bpy

from .. import utils


# Panel
class PanelRandomMaterialNodes(bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    # TODO: are these docstrings shown in the UI as tooltips somewhere?

    # metadata
    bl_idname = "NODE_MATERIAL_PT_random"
    bl_label = "Randomise MATERIAL"  # title of the panel displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        # draw the panel only if there is an active material
        # for the selected object
        return context.object.active_material is not None

    def draw(self, context):
        # Get list of input nodes to randomise
        # for currently active material
        list_input_nodes = utils.get_material_input_nodes_to_randomise(
            context.object.active_material.name
        )

        # Get collection of sockets' properties
        # 'context.scene.sockets2randomise_props.update_collection'
        # triggers the get function that checks if an update is
        # required. If it is, the collection of sockets is updated
        # and 'context.scene.sockets2randomise_props.update_collection'
        # returns TRUE
        cs = context.scene
        if cs.sockets2randomise_props.update_collection:
            print("Collection of sockets updated")
        sockets_props_collection = cs.sockets2randomise_props.collection

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
                for m_str, col in zip(["min", "max"], [col3, col4]):
                    # if socket is a color: format min/max as a color picker
                    # and an array (color picker doesn't include alpha value)
                    if type(sckt) == bpy.types.NodeSocketColor:
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

        # add randomise button for operator
        row = layout.row(align=True)
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)
        col3 = row_split.column(align=True)
        col4 = row_split.column(align=True)
        col5 = row_split.column(align=True)
        col5.operator("node.randomise_socket", text="Randomise")


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PanelRandomMaterialNodes,
]


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("material UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material UI unregistered")
