from random import seed

import bpy

# from utils import nodes2rand

# @persistent
# def randomise_camera_transform_per_frame(dummy):
#     bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
#     return


bpy.data.scenes["Scene"].seed_properties.seed_toggle = True
bpy.data.scenes["Scene"].seed_properties.seed = 3
seed(3)
bpy.data.scenes["Scene"].frame_current = 0
sequence_length = 7
first_run = []
second_run = []

# bpy.app.handlers.frame_change_pre.append(
#         randomise_camera_transform_per_frame
#     )

# bpy.app.handlers.frame_change_pre.append(
#         randomise_geometry_nodes_per_frame
#     )


for idx in range(sequence_length):
    bpy.app.handlers.frame_change_pre[0](
        "dummy"
    )  # on own number stays the same
    #    bpy.app.handlers.frame_change_pre.append(randomise_geometry_nodes_per_frame)
    # with both number is same for all 5 frames but changes each time
    print("handlesrs", bpy.app.handlers.frame_change_pre)

    bpy.data.scenes["Scene"].frame_current = idx
    print("frame = ", bpy.data.scenes["Scene"].frame_current)
    print("pos x = ", bpy.data.objects["Camera"].location[0])
    print(
        "geom = ",
        bpy.data.node_groups[0]
        .nodes["RandomConeDepth"]
        .outputs[0]
        .default_value,
    )
    first_run.append(bpy.data.objects["Camera"].location[0])
    bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")
    second_run.append(
        bpy.data.node_groups[0]
        .nodes["RandomConeDepth"]
        .outputs[0]
        .default_value
    )

data = {
    "transform_x": first_run,
    "geometry": second_run,
}
print(data)
# path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"
# print(path_to_file)

# with open(path_to_file, "w") as out_file_obj:
#     # convert the dictionary into text
#     text = json.dumps(data, indent=4)
#     # write the text into the file
#     out_file_obj.write(text)


#### SUBPANEL materials
# Get list of input nodes to randomise
# for this subpanel's material
# cs = bpy.context.scene
# subpanel_material = cs.socket_props_per_material.collection[0]
# list_input_nodes = nodes2rand.get_material_nodes_to_randomise_indep(
#     subpanel_material.name
# )


def draw_sockets_list(
    cs,
    list_input_nodes,
):
    # Define UI fields for every socket property
    # NOTE: if I don't sort the input nodes, everytime one of the nodes is
    # selected in the graph it moves to the bottom of the panel.
    list_input_nodes_sorted = sorted(list_input_nodes, key=lambda x: x.name)
    for i_n, nd in enumerate(list_input_nodes_sorted):
        # add sockets for this node in the subseq rows
        for sckt in nd.outputs:
            print(
                getattr(
                    sckt,
                    "default_value",
                )
            )


#            col1.label(text=sckt.name)


# socket current value
#            col2.prop(
#                sckt,
#                "default_value",
#                icon_only=True,
#            )
#            col2.enabled = False  # current value is not editable


#### SUBSUBPANEL
# def draw(self, context):
# cs = bpy.context.scene

#        # then force an update in the sockets per material
#        # TODO: do I need this? it should update when drawing the subpanel
# if cs.socket_props_per_material.collection[
#        self.subpanel_material_str
#    ].update_sockets_collection:
#        print("Collection of sockets updated")

#    # get (updated) collection of socket properties
#    # for the current material
# sockets_props_collection = cs.socket_props_per_material.collection[
#    self.subpanel_material_str
# ].collection

## Get list of input nodes to randomise
## for this subpanel's material
## only nodes inside groups!
## keep only nodes inside this group!
# list_input_nodes = [
#    nd
#    for nd in self.list_nodes2rand_in_groups
#    if nd.id_data.name == self.group_node_name
# ]

# def draw_sockets_list(
#    cs,
#    layout,
#    list_input_nodes,
#    sockets_props_collection,
# ):
#    # Define UI fields for every socket property
#    # NOTE: if I don't sort the input nodes, everytime one of the nodes is
#    # selected in the graph it moves to the bottom of the panel.
#    list_input_nodes_sorted = sorted(list_input_nodes, key=lambda x: x.name)
#    for i_n, nd in enumerate(list_input_nodes_sorted):
#        row = layout.row()

#        # if first node: add labels for
#        # name, min, max and randomisation toggle
#        if i_n == 0:
#            row_split = row.split()
#            col1 = row_split.column(align=True)
#            col2 = row_split.column(align=True)
#            col3 = row_split.column(align=True)
#            col4 = row_split.column(align=True)
#            col5 = row_split.column(align=True)

#            # input node name
#            col1.label(text=nd.name)
#            col1.alignment = "CENTER"

#            # min label
#            col3.alignment = "CENTER"
#            col3.label(text="min")

#            # max label
#            col4.alignment = "CENTER"
#            col4.label(text="max")

#        # if not first node: add just node name
#        else:
#            row.separator(factor=1.0)  # add empty row before each node
#            row = layout.row()

#            row.label(text=nd.name)

#        # add sockets for this node in the subseq rows
#        for sckt in nd.outputs:
#            # split row in 5 columns
#            row = layout.row()
#            row_split = row.split()
#            col1 = row_split.column(align=True)
#            col2 = row_split.column(align=True)
#            col3 = row_split.column(align=True)
#            col4 = row_split.column(align=True)
#            col5 = row_split.column(align=True)

#            # socket name
#            col1.alignment = "RIGHT"
#            col1.label(text=sckt.name)

#            # socket current value
#            col2.prop(
#                sckt,
#                "default_value",
#                icon_only=True,
#            )
#            col2.enabled = False  # current value is not editable

#            # socket min and max columns
#            socket_id = nd.name + "_" + sckt.name
#            if (nd.id_data.name in bpy.data.node_groups) and (
#                bpy.data.node_groups[nd.id_data.name].type == "SHADER"
#            ):  # only for SHADER groups
#                socket_id = nd.id_data.name + "_" + socket_id

#            # if socket is a color: format min/max as a color picker
#            # and an array (color picker doesn't include alpha value)
#            if type(sckt) == bpy.types.NodeSocketColor:
#                for m_str, col in zip(["min", "max"], [col3, col4]):
#                    # color picker
#                    col.template_color_picker(
#                        sockets_props_collection[socket_id],
#                        m_str + "_" + cs.socket_type_to_attr[type(sckt)],
#                    )
#                    # array
#                    for j, cl in enumerate(["R", "G", "B", "alpha"]):
#                        col.prop(
#                            sockets_props_collection[socket_id],
#                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
#                            icon_only=False,
#                            text=cl,
#                            index=j,
#                        )
#            # if socket is Boolean: add non-editable labels
#            elif type(sckt) == bpy.types.NodeSocketBool:
#                for m_str, col in zip(["min", "max"], [col3, col4]):
#                    m_val = getattr(
#                        sockets_props_collection[socket_id],
#                        m_str + "_" + cs.socket_type_to_attr[type(sckt)],
#                    )
#                    col.label(text=str(list(m_val)[0]))

#            # if socket is not color type: format as a regular property
#            else:
#                for m_str, col in zip(["min", "max"], [col3, col4]):
#                    col.prop(
#                        sockets_props_collection[socket_id],
#                        m_str + "_" + cs.socket_type_to_attr[type(sckt)],
#                        icon_only=True,
#                    )

#            # randomisation toggle
#            col5.prop(
#                sockets_props_collection[socket_id],
#                "bool_randomise",
#                icon_only=True,
#            )
