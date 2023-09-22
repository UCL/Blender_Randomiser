from random import seed

import bpy

if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
    seed(bpy.data.scenes["Scene"].seed_properties.seed)

bpy.data.scenes["Scene"].frame_current = 0
tot_frame_no = bpy.context.scene.rand_all_properties.tot_frame_no
x_pos_vals = []
y_pos_vals = []
z_pos_vals = []


x_rot_vals = []
y_rot_vals = []
z_rot_vals = []

if bpy.context.scene.randomise_camera_props.bool_delta:
    loc_value_str = "delta_location"
    value_str = "delta_rotation_euler"
else:
    loc_value_str = "location"
    value_str = "rotation_euler"

geom = []
for idx in range(tot_frame_no):
    bpy.app.handlers.frame_change_pre[0]("dummy")
    bpy.data.scenes["Scene"].frame_current = idx

    x_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[0])
    y_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[1])
    z_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[2])

    x_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[0])
    y_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[1])
    z_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[2])

    bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")
    geom.append(
        bpy.data.node_groups[0]
        .nodes["RandomConeDepth"]
        .outputs[0]
        .default_value
    )

data = {
    "location_str": loc_value_str,
    "loc_x": x_pos_vals,
    "loc_y": y_pos_vals,
    "loc_z": z_pos_vals,
    "rotation_str": value_str,
    "rot_x": x_rot_vals,
    "rot_y": y_rot_vals,
    "rot_z": z_rot_vals,
    "geometry": geom,
}
print(data)
# path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"
# print(path_to_file)

# with open(path_to_file, "w") as out_file_obj:
#     # convert the dictionary into text
#     text = json.dumps(data, indent=4)
#     # write the text into the file
#     out_file_obj.write(text)


# path_to_file = pathlib.Path.home() / "tmp" / "input_parameters.json"
#### TODO check file exists
# with open(path_to_file, "r") as in_file_obj:
#    text = in_file_obj.read()
#    # convert the text into a dictionary
#    data = json.loads(text)


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
