"""
Solution to show all materials in subpanels inspired on this SO answer:
https://blender.stackexchange.com/questions/185693/how-can-i-control-the-number-of-sub-panel-instances-from-an-intproperty

"""
import bpy

from .. import utils

MAX_NUMBER_OF_PANELS = 100


# ----------------------
# Main panel
# ---------------------
class TemplatePanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"  # this shows up as the tab name


class MainPanelRandomMaterialNodes(TemplatePanel, bpy.types.Panel):
    bl_idname = "NODE_MATERIAL_PT_mainpanel"
    bl_label = "Randomise MATERIAL"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select material to see available sockets.")


# ------------------------------
# Subpanel for active material
# -----------------------------
class SubPanelRandomMaterialNodes(TemplatePanel, bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    bl_idname = (
        "NODE_MATERIAL_PT_subpanel"  # what is this for? --internal reference?
    )
    bl_parent_id = "NODE_MATERIAL_PT_mainpanel"  # use bl_idname
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        # RN: Only display if
        # - there is an active material, and
        # - the active material is in the collection

        # For subpanels for all materials: Only display if
        # - subpanel material index is lower than the length of
        # the list of materials
        cs = context.scene
        # cob = context.object

        # subpanel_material = cs.socket_props_per_material.candidate_materials[
        #     self.subpanel_material_idx
        # ]

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
            # list of materials in collection
        )

        # draw the panel only if there is an active material
        # for the selected object, and if this material is in
        # the materials collection (i.e., if 'use_nodes' is True
        # for this material)
        # NOTE: the active material may not be in the collection if
        # use_nodes is unticked
        # return (cob.active_material is not None) and (
        #     cob.active_material.name
        #     in cs.socket_props_per_material.collection
        # )

    def draw_header(self, context):
        cs = context.scene
        layout = self.layout

        # TODO: maybe a dict? can order change?
        subpanel_material = cs.socket_props_per_material.candidate_materials[
            self.subpanel_material_idx
        ]

        layout.label(text=subpanel_material.name)

    def draw(self, context):
        # material for this subpanel
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.candidate_materials[
            self.subpanel_material_idx
        ]
        subpanel_material_name = subpanel_material.name

        # Get list of input nodes to randomise
        # for this subpanel's material
        list_input_nodes = utils.get_material_input_nodes_to_randomise(
            subpanel_material_name
        )

        # then force an update in the sockets per material
        # subpanel_material_name = subpanel_material.name
        if cs.socket_props_per_material.collection[
            subpanel_material_name
        ].update_sockets_collection:
            print("Collection of sockets updated")

        # get (updated) collection of socket properties
        # for the current material
        sockets_props_collection = cs.socket_props_per_material.collection[
            subpanel_material_name
        ].collection

        # Define UI fields for every socket property
        # NOTE: if I don't sort the input nodes, everytime one of the nodes is
        # selected in the graph it moves to the bottom of the panel (?).
        # TODO: sort by date of creation? ---I didn't find an easy way to do it
        layout = self.layout
        for i_n, nd in enumerate(
            sorted(list_input_nodes, key=lambda x: x.name)
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

        # add randomise button for operator at the end
        # (only if there are input nodes)
        if list_input_nodes:
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
    MainPanelRandomMaterialNodes,
    # SubPanelRandomMaterialNodes,
]

# add subpanels per i to list of classes to register
for i in range(MAX_NUMBER_OF_PANELS):
    subpanel_class_i = type(
        f"NODE_MATERIAL_PT_subpanel_{i}",
        (
            SubPanelRandomMaterialNodes,
            bpy.types.Panel,
        ),  # parent classes (is Panel req?)
        {
            "bl_idname": f"NODE_MATERIAL_PT_subpanel_{i}",
            # "bl_label": "",
            #  I change title of subpanel this via draw_header
            "subpanel_material_idx": i,
        },
    )
    list_classes_to_register.append(subpanel_class_i)  # type: ignore


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("material UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material UI unregistered")
