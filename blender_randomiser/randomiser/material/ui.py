import bpy

from .. import utils


# -------
# Panel
class PanelRandomMaterialNodes(bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_random"
    bl_label = "Randomise material nodes"
    # title of the panel / label displayed to the user
    bl_space_type = (
        "NODE_EDITOR"  # "VIEW_3D" instead? "PROPERTIES" and "WINDOW" instead?
    )
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        # TODO: is the object context what I need to check?
        return context.object is not None

    def draw(self, context):
        # Get list of input nodes to randomise
        list_input_nodes = utils.get_material_input_nodes_to_randomise()

        # get collection of sockets' properties
        # the expression 'context.scene.update_collection_socket_props'
        # triggers the get fn that checks if an update is req and if so,
        # updates the collection of sockets and returns TRUE
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
                col2.enabled = False  # (not editable)

                # socket min and max columns
                socket_id = nd.name + "_" + sckt.name
                for m_str, col in zip(["min", "max"], [col3, col4]):
                    # if color socket: format as a color wheel
                    if type(sckt) == bpy.types.NodeSocketColor:
                        # show color property via color picker
                        # ATT! It doesn't include alpha!
                        col.template_color_picker(
                            sockets_props_collection[socket_id],
                            m_str
                            + "_"
                            + cs.socket_type_to_attr[type(sckt)],  # property
                        )
                        # show color property as an array too (including alpha)
                        for j, cl in enumerate(["R", "G", "B", "alpha"]):
                            col.prop(
                                sockets_props_collection[socket_id],
                                m_str
                                + "_"
                                + cs.socket_type_to_attr[
                                    type(sckt)
                                ],  # property
                                icon_only=False,
                                text=cl,
                                index=j,
                                # ATT! if I pass -1 it will use all
                                # elements of the array (rather than
                                # the last one)
                            )
                    # if not color socket: format as a regular prop
                    else:
                        col.prop(
                            sockets_props_collection[socket_id],
                            m_str
                            + "_"
                            + cs.socket_type_to_attr[type(sckt)],  # property
                            icon_only=True,
                        )

                # randomisation toggle
                col5.prop(
                    sockets_props_collection[socket_id],
                    "bool_randomise",
                    icon_only=True,
                )

        # add Randomise button
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
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material UI unregistered")
