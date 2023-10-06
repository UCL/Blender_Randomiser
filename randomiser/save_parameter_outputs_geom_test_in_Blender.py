import json
import pathlib
from random import seed

import bpy

### GEOMETRY
# collection[N].collection[S]
# [N] = 0, 1, 2 for each node group (even NG within NG)
# [S] = 0, 1 etc. for each socket within node group
# Actual Geom values followed by Min_Max
# Node group called "Geometry Nodes"
bpy.data.node_groups["Geometry Nodes"].nodes["RandomConeDepth"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
    0
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
    0
].max_float_1d[0]

bpy.data.node_groups["Geometry Nodes"].nodes["RandomRadiusBottom"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
    1
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
    1
].max_float_1d[0]


# Node group called "NodeGroup" which is associated
# with "Geometry Nodes" node group
bpy.data.node_groups["NodeGroup"].nodes["RandomConeDepth.001"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_gng.collection[1].collection[
    0
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_gng.collection[1].collection[
    0
].max_float_1d[0]

bpy.data.node_groups["NodeGroup"].nodes["RandomRadiusBottom.001"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_gng.collection[1].collection[
    1
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_gng.collection[1].collection[
    1
].max_float_1d[0]

# Separate node group called "Geometry Nodes.001"
bpy.data.node_groups["Geometry Nodes.001"].nodes["RandomSize"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_gng.collection[2].collection[
    0
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_gng.collection[2].collection[
    0
].max_float_1d[0]


### MATERIALS
# collection[N].collection[S]
# [N] = 0 "Material.001"
# [S] = 0 RandomMetallic, = 1 RandomBaseRGB
# [N] = 1 "Material" and "NodeGroup.001"
# [S] = 0 "RandomMetallic.001", 1 = RandomMetallic
# [S] = 2 "RandomBaseRGB.001", 3 RandomBaseRGB
# Actual Mat values followed by Min_Max
# Material called "Material" containing node_tree.nodes
bpy.data.materials["Material"].node_tree.nodes["RandomMetallic"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_material.collection[1].collection[
    1
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_material.collection[1].collection[
    1
].max_float_1d[0]

bpy.data.materials["Material"].node_tree.nodes["RandomBaseRGB"].outputs[
    0
].default_value
# bpy.data.scenes['Scene'].socket_props_per_material.collection[1].collection[3].min_rgba_4d[0-3]
# bpy.data.scenes['Scene'].socket_props_per_material.collection[1].collection[3].max_rgba_4d[0-3]


# Node group called "NodeGroup.001" which is associated
# with "Material" material
bpy.data.node_groups["NodeGroup.001"].nodes["RandomMetallic.001"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_material.collection[1].collection[
    0
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_material.collection[1].collection[
    0
].max_float_1d[0]

bpy.data.node_groups["NodeGroup.001"].nodes["RandomBaseRGB.001"].outputs[
    0
].default_value
# bpy.data.scenes['Scene'].socket_props_per_material.collection[1].collection[2].min_rgba_4d[0-3]
# bpy.data.scenes['Scene'].socket_props_per_material.collection[1].collection[2].max_rgba_4d[0-3]


# Separate material called "Material.001" containing node_tree.nodes
bpy.data.materials["Material.001"].node_tree.nodes["RandomMetallic"].outputs[
    0
].default_value
bpy.data.scenes["Scene"].socket_props_per_material.collection[0].collection[
    0
].min_float_1d[0]
bpy.data.scenes["Scene"].socket_props_per_material.collection[0].collection[
    0
].max_float_1d[0]

bpy.data.materials["Material.001"].node_tree.nodes["RandomBaseRGB"].outputs[
    0
].default_value
# bpy.data.scenes['Scene'].socket_props_per_material.collection[0].collection[1].min_rgba_4d[0-3]
# bpy.data.scenes['Scene'].socket_props_per_material.collection[0].collection[1].max_rgba_4d[0-3]


# Min-max Geom values

if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
    seed(bpy.data.scenes["Scene"].seed_properties.seed)


### ALL
tot_frame_no = bpy.context.scene.rand_all_properties.tot_frame_no

### TRANSFORMS
bpy.data.scenes["Scene"].frame_current = 0

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


geom_single_test = []
mat_single_test = []
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
    geom_single_test.append(
        bpy.data.node_groups[0]
        .nodes["RandomConeDepth"]
        .outputs[0]
        .default_value
    )

    bpy.ops.node.randomise_all_material_sockets("INVOKE_DEFAULT")
    mat_single_test.append(
        bpy.data.materials["Material"]
        .node_tree.nodes["RandomMetallic"]
        .outputs[0]
        .default_value
    )


### GEOMETRY
bpy.data.scenes["Scene"].frame_current = 0
# geom ={'0': []}
# print(geom)
# for i in range(len(bpy.context.scene.socket_props_per_gng.collection)):
#     if i>=1:
#         geom[str(i)]=[]

# print(geom)

# mat ={'0': []}
# for i in range(len(bpy.context.scene.socket_props_per_material.collection)):
#     if i>=1:
#         mat[str(i)]=[]

# all_geom=[]
# bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].name
# bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[0].name
all_geom_dict = {}
cs = bpy.context.scene
for gng_idx in range(len(cs.socket_props_per_gng.collection)):
    # get this subpanel's GNG
    subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]
    tmp_GNG = subpanel_gng.name
    print(tmp_GNG)

    sockets_props_collection = cs.socket_props_per_gng.collection[
        subpanel_gng.name
    ].collection

    list_parent_nodes_str = [
        sckt.name.split("_")[0] for sckt in sockets_props_collection
    ]
    list_input_nodes = [
        bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
        for nd_str in list_parent_nodes_str
    ]

    list_input_nodes_sorted = sorted(list_input_nodes, key=lambda x: x.name)
    for i_n, nd in enumerate(list_input_nodes_sorted):
        # add sockets for this node in the subseq rows
        for sckt in nd.outputs:
            print("i_n", i_n)
            print("nd", nd)
            print(
                getattr(
                    sckt,
                    "default_value",
                )
            )

            tmp_values = []
            for idx in range(tot_frame_no):
                bpy.app.handlers.frame_change_pre[0]("dummy")
                bpy.data.scenes["Scene"].frame_current = idx
                bpy.ops.node.randomise_all_geometry_sockets(
                    "INVOKE_DEFAULT"
                )  # issue
                # w/ this being called so often -
                # might need moved to diff for loop?
                tmp_values.append(
                    getattr(
                        sckt,
                        "default_value",
                    )
                )

            print(tmp_values)
            tmp_sck = nd.name
            all_geom_dict[tmp_GNG] = tmp_sck
            GNG_sck_values_str = tmp_GNG + tmp_sck
            GNG_sck_values_str = "Values " + GNG_sck_values_str
            print(GNG_sck_values_str)
            all_geom_dict[GNG_sck_values_str] = tmp_values

    # for sck_idx in range(len(subpanel_gng.collection)):
    #     tmp_sck = subpanel_gng.collection[sck_idx].name
    #     if "_Value" in tmp_sck:
    #         tmp_sck=tmp_sck.replace("_Value", "")

    #     print(tmp_sck)
    #     tmp_values = []

    # for idx in range(tot_frame_no):
    #     bpy.app.handlers.frame_change_pre[0]("dummy")
    #     bpy.data.scenes["Scene"].frame_current = idx
    #     bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT") # issue
    # w/ this being called so often - might need moved to diff for loop?
    #     tmp_values.append(
    #         bpy.data.node_groups[tmp_GNG]
    #         .nodes[tmp_sck]
    #         .outputs[0]
    #         .default_value
    #     )

    # print(tmp_values)
    # all_geom_dict[tmp_GNG] = tmp_sck
    # GNG_sck_values_str = tmp_GNG + tmp_sck
    # GNG_sck_values_str = 'Values ' + GNG_sck_values_str
    # print(GNG_sck_values_str)
    # all_geom_dict[GNG_sck_values_str] = tmp_values


print(all_geom_dict)

#### THIS IS FINE AS IT IS (dict within dict
# for geometry and materials

data = {
    "location_str": loc_value_str,
    "loc_x": x_pos_vals,
    "loc_y": y_pos_vals,
    "loc_z": z_pos_vals,
    "rotation_str": value_str,
    "rot_x": x_rot_vals,
    "rot_y": y_rot_vals,
    "rot_z": z_rot_vals,
    "geometry": all_geom_dict,
    "materials": mat_single_test,
}
# print(data)
path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"
print(path_to_file)

with open(path_to_file, "w") as out_file_obj:
    # convert the dictionary into text
    text = json.dumps(data, indent=4)
    # write the text into the file
    out_file_obj.write(text)


# path_to_file = pathlib.Path.home() / "tmp" / "input_parameters.json"
#### TODO check file exists
# with open(path_to_file, "r") as in_file_obj:
#    text = in_file_obj.read()
#    # convert the text into a dictionary
#    data = json.loads(text)


#### SUBPANEL materials


##### Function called by main code
def get_material_nodes_to_randomise_indep(
    material_str: str = "Material",
    node2randomise_prefix: str = "random",
):
    """Get list of *independent* input nodes to randomise for a given material.

    Input nodes are defined as nodes with no input sockets.
    The input nodes to randomise are identified because their
    name is prefixed with node2randomise_prefix (case insensitive).

    Both independent nodes, and nodes inside a group are searched.
    The 'artificial' nodes that show up inside a node group, usually named
    'Group input' or 'Group output' are excluded from the search.

    Parameters
    ----------
    material_str : str, optional
        name of the material, by default "Material"
    node2randomise_prefix : str, optional
        prefix that identifies the nodes to randomise, by default 'random'

    Returns
    -------
    list
        list of all *group* input nodes to randomise for this material
    """

    # list of nodes for current material
    # not belonging to a group
    list_material_nodes_indep = []
    for nd in bpy.data.materials[material_str].node_tree.nodes:
        if nd.type != "GROUP":
            list_material_nodes_indep.append(nd)

    # find input nodes that startwith random
    list_input_nodes = get_nodes_to_randomise_from_list(
        list_material_nodes_indep
    )

    return list_input_nodes


### Called by get_material_nodes_to_randomise_indep
def get_nodes_to_randomise_from_list(
    list_candidate_nodes: list,
    node2randomise_prefix: str = "random",
):
    """Get list of nodes to randomise from list.

    Input nodes are defined as nodes with no input sockets.
    The nodes to randomise are input nodes whose name starts
    with 'node2randomise_prefix' (case insensitive).

    The 'artificial' nodes that show up inside a node group, usually named
    'Group input' or 'Group output' are excluded from the search.

    Parameters
    ----------
    list_candidate_nodes : list
        list of the candidate nodes to randomise
    node2randomise_prefix : str, optional
        prefix that identifies the nodes to randomise, by default 'random'

    Returns
    -------
    list
        list of the input nodes to randomise
    """

    # ensure list_candidate_nodes is unique
    list_candidate_nodes = list(set(list_candidate_nodes))

    # find input nodes that start with the random keyword
    # excluding 'Group' artificial nodes
    list_input_nodes = [
        nd
        for nd in list_candidate_nodes
        if len(nd.inputs) == 0
        and nd.name.lower().startswith(node2randomise_prefix.lower())
        and nd.type
        not in [
            "GROUP_INPUT",
            "GROUP_OUTPUT",
        ]
    ]

    return list_input_nodes


#### MAIN CODE TO REPLICATE FROM ui.py Get material nodes
# (in our case want to automate node socket, no need to draw socket)
# Get list of input nodes to randomise
# for this subpanel's material
cs = bpy.context.scene
subpanel_material = cs.socket_props_per_material.collection[0]
list_input_nodes = get_material_nodes_to_randomise_indep(
    subpanel_material.name
)
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

#### MAIN CODE TO REPLICATE ui.py GEOM
cs = bpy.context.scene

# get this subpanel's GNG
subpanel_gng = cs.socket_props_per_gng.collection[0]  # self.subpanel_gng_idx

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
    list_input_nodes,
)


##### NEW CODE refactoring code from above
print("NEW CODE material starts here")
cs = bpy.context.scene
subpanel_material = cs.socket_props_per_material.collection[0]
list_input_nodes = get_material_nodes_to_randomise_indep(
    subpanel_material.name
)

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

print(len(list_input_nodes_sorted))

print("NEW CODE geometry starts here")
cs = bpy.context.scene
# get this subpanel's GNG
subpanel_gng = cs.socket_props_per_gng.collection[0]  # self.subpanel_gng_idx
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

print(len(list_input_nodes_sorted))


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
