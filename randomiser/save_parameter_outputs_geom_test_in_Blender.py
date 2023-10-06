import json
import pathlib
from random import seed

# from .utils import nodes2rand
import bpy


def get_material_nodes_to_randomise_all(
    material_str: str = "Material",
    node2randomise_prefix: str = "random",
):
    """Get list of all input nodes to randomise for a given material.

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
        list of the input nodes to randomise
    """

    # find input nodes that startwith random
    # in any of those groups
    # excluding 'Group' nodes
    list_indep_input_nodes = get_material_nodes_to_randomise_indep(
        material_str, node2randomise_prefix
    )

    list_group_input_nodes = get_material_nodes_to_randomise_group(
        material_str, node2randomise_prefix
    )

    return list_indep_input_nodes + list_group_input_nodes


def get_node_group_parent_of_node_group(node_group):
    # input node group could be a material, in which case the
    # node group parent is none
    parent_ng = None

    if node_group is not None and (type(node_group) != bpy.types.Material):
        list_all_ngs = [
            gr for gr in bpy.data.node_groups if gr.type == node_group.type
        ]

        for gr in list_all_ngs:
            for nd in gr.nodes:
                if (
                    (hasattr(nd, "node_tree"))
                    and (hasattr(nd.node_tree, "name"))
                    and (nd.node_tree.name == node_group.name)
                ):
                    parent_ng = gr
                    break

    return parent_ng  # immediate parent


def get_parent_of_gng(
    node_group,
):
    """Get immediate parent of geometry node group.

    Returns the node tree that the input geometry node group is
    inside of.

    If the input geometry node group has no parent (i.e., it is a root node)
    this function will return None for its parent

    Parameters
    ----------
    node_group : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # the parent of a GNG can only be another GNG, or None
    return get_node_group_parent_of_node_group(node_group)


def get_parent_of_sng(node_group):
    """Get immediate parent of shader node group.

    Returns the node tree that the input shader node group is
    inside of. The top parent of a shader node group would be a material.

    The parent of a material is None. The parent of a node group
    that is not linked to a material is also None?

    Parameters
    ----------
    node_group : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    # the parent of a SNG can be another SNG, a Material, or None
    # input node group could be a material, in which case the parent is none

    # check if parent is a node group
    parent_sng = get_node_group_parent_of_node_group(node_group)

    # if the input node group is NOT a material:
    # check further if parent is a material
    if (
        (parent_sng is None)
        and (node_group is not None)
        and (type(node_group) is not bpy.types.Material)
    ):
        list_all_materials = [
            mat for mat in bpy.data.materials if mat.use_nodes
        ]
        # TODO: is it possible that a material has no node_tree?
        # (I think maybe, if use_nodes is set to False)
        # TODO: use candidate_materials property?
        for mat in list_all_materials:
            for nd in mat.node_tree.nodes:
                if (
                    (nd.type == "GROUP")
                    and (hasattr(nd, "node_tree"))
                    and (hasattr(nd.node_tree, "name"))
                    and (nd.node_tree.name == node_group.name)
                ):
                    parent_sng = mat
                    break

    return parent_sng  # immediate parent


def get_parent_of_ng(node_group):
    # Select the function to compute the parent of the
    # node group based on the node group type
    if (type(node_group) == bpy.types.Material) or (
        node_group.type == "SHADER"
    ):
        return get_parent_of_sng(node_group)
    elif node_group.type == "GEOMETRY":
        return get_parent_of_gng(node_group)


def get_root_and_depth_of_ng(node_group):
    # TODO: combine this with path?

    # compute root node group: this is the node group in
    # the path whose parent is None. For shader node groups,
    # it will be the material
    parent = get_parent_of_ng(node_group)
    depth = 0
    if parent is None:
        return (parent, depth)
    else:
        depth = 1
        while get_parent_of_ng(parent) is not None:
            depth += 1
            parent = get_parent_of_ng(parent)

    return (parent, depth)


def get_map_inner_ngs_given_roots(
    list_candidate_roots,
):
    """Compute dictionary that maps inner node groups to a tuple made of
    - the inner node group's root parent (a node group, a material, or None)
    - the inner node group's depth

    The dictionary is computed for inner node groups whose root parents
    are in the input list

    Parameters
    ----------
    list_candidate_root_node_groups : _type_
        list of node groups
    """
    # TODO: check in inputs are inded roots and print warning if not?
    list_node_groups = [
        gr for gr in bpy.data.node_groups  # if gr.type == "GEOMETRY"
    ]

    map_node_group_to_root = {}
    for gr in list_node_groups:
        root_parent, depth = get_root_and_depth_of_ng(gr)
        if root_parent in list_candidate_roots:
            map_node_group_to_root[gr] = (root_parent, depth)  # tuple

    return map_node_group_to_root


def get_path_to_ng(node_group):
    """Compute path of parent group nodes up
    to the input group node

    Both the root parent and the input
    group node are included, except if the root parent is None

    Parameters
    ----------
    gng : _type_
        inner geometry group need of which we want to
        obtain the path

    Returns
    -------
    path_to_ng: list
        a list of parent geometry group nodes up to the input one
    """
    parent = get_parent_of_ng(node_group)
    if parent is None:
        path_to_ng = []  # why empty rather than [None]?
    else:
        path_to_ng = [parent]
        while get_parent_of_ng(parent) is not None:
            parent = get_parent_of_ng(parent)
            path_to_ng.append(parent)

        path_to_ng.reverse()

    path_to_ng.append(node_group)
    return path_to_ng


def get_max_depth_of_root(root_parent_node_group):
    """Compute the maximum depth of any inner geometry group
    for the given root parent node group

    A root parent node group is a node group or a Material whose
    parent is None

    Parameters
    ----------
    root_parent_node_group : _type_
        root parent node group of which we want to compute the
        maximum depth

    Returns
    -------
    max_depth : int
        the depth of the innermost node group
        for this root parent node group
    """
    map_inner_ngs = get_map_inner_ngs_given_roots([root_parent_node_group])

    max_depth = 0
    if map_inner_ngs:
        max_depth = max([v[1] for _, v in map_inner_ngs.items()])

    return max_depth


def get_material_nodes_to_randomise_group(
    material_str: str = "Material",
    node2randomise_prefix: str = "random",
):
    """Get list of *group* input nodes to randomise for a given material.

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
    # belonging to a group; the group can be any levels deep

    # list of inner node groups for this material
    map_inner_node_groups = get_map_inner_ngs_given_roots(
        [bpy.data.materials[material_str]]
    )
    list_inner_node_groups = list(map_inner_node_groups.keys())

    # list of all material nodes inside a group
    list_material_nodes_in_groups = []
    for ng in list_inner_node_groups:
        list_material_nodes_in_groups.extend(ng.nodes)  # nodes inside groups

    # find input nodes that startwith random
    # in any of those groups
    # excluding 'Group' nodes
    list_input_nodes = get_nodes_to_randomise_from_list(
        list_material_nodes_in_groups
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


### ALL
if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
    seed(bpy.data.scenes["Scene"].seed_properties.seed)
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

### MATERIALS
bpy.data.scenes["Scene"].frame_current = 0
all_mat_dict = {}
cs = bpy.context.scene
for mat_idx in range(len(cs.socket_props_per_material.collection)):
    # get this subpanel's GNG
    subpanel_material = cs.socket_props_per_material.collection[mat_idx]
    tmp_mat = subpanel_material.name
    print(tmp_mat)

    list_input_nodes = get_material_nodes_to_randomise_indep(
        subpanel_material.name
    )

    list_nodes2rand_in_groups = get_material_nodes_to_randomise_group(
        subpanel_material.name
    )

    list_input_nodes_all = get_material_nodes_to_randomise_all(
        subpanel_material.name
    )

    print("list_input_nodes ====== ", list_input_nodes)
    print("list nodes2rand in groups ===== ", list_nodes2rand_in_groups)
    print("list_input_nodes_all ===== ", list_input_nodes_all)

    list_input_nodes_sorted = sorted(
        list_input_nodes_all, key=lambda x: x.name
    )
    for i_n, nd in enumerate(list_input_nodes_sorted):
        # add sockets for this node in the subseq rows
        for sckt in nd.outputs:
            print(nd.name)
            print(
                getattr(
                    sckt,
                    "default_value",
                )
            )

            test_attr = getattr(
                sckt,
                "default_value",
            )
            print(str(test_attr))

            if "NodeSocketColor" not in str(test_attr):
                print("NODESOCKETCOLOR", str(test_attr))
                tmp_values = []
                for idx in range(tot_frame_no):
                    bpy.app.handlers.frame_change_pre[0]("dummy")
                    bpy.data.scenes["Scene"].frame_current = idx
                    bpy.ops.node.randomise_all_material_sockets(
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
                all_mat_dict[tmp_mat] = tmp_sck
                MAT_sck_values_str = tmp_mat + tmp_sck
                MAT_sck_values_str = "Values " + MAT_sck_values_str
                print(MAT_sck_values_str)
                all_mat_dict[MAT_sck_values_str] = tmp_values

# print(all_mat_dict)

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
    "materials": all_mat_dict,
}
# print(data)
path_to_file = pathlib.Path.home() / "tmp" / "transform_geom_mat_test.json"
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


# ##### Function called by main code
# def get_material_nodes_to_randomise_indep(
#     material_str: str = "Material",
#     node2randomise_prefix: str = "random",
# ):
#     """Get list of *independent* input nodes to
# randomise for a given material.

#     Input nodes are defined as nodes with no input sockets.
#     The input nodes to randomise are identified because their
#     name is prefixed with node2randomise_prefix (case insensitive).

#     Both independent nodes, and nodes inside a group are searched.
#     The 'artificial' nodes that show up inside a node group, usually named
#     'Group input' or 'Group output' are excluded from the search.

#     Parameters
#     ----------
#     material_str : str, optional
#         name of the material, by default "Material"
#     node2randomise_prefix : str, optional
#         prefix that identifies the nodes to randomise, by default 'random'

#     Returns
#     -------
#     list
#         list of all *group* input nodes to randomise for this material
#     """

#     # list of nodes for current material
#     # not belonging to a group
#     list_material_nodes_indep = []
#     for nd in bpy.data.materials[material_str].node_tree.nodes:
#         if nd.type != "GROUP":
#             list_material_nodes_indep.append(nd)

#     # find input nodes that startwith random
#     list_input_nodes = get_nodes_to_randomise_from_list(
#         list_material_nodes_indep
#     )

#     return list_input_nodes


# ### Called by get_material_nodes_to_randomise_indep
# def get_nodes_to_randomise_from_list(
#     list_candidate_nodes: list,
#     node2randomise_prefix: str = "random",
# ):
#     """Get list of nodes to randomise from list.

#     Input nodes are defined as nodes with no input sockets.
#     The nodes to randomise are input nodes whose name starts
#     with 'node2randomise_prefix' (case insensitive).

#     The 'artificial' nodes that show up inside a node group, usually named
#     'Group input' or 'Group output' are excluded from the search.

#     Parameters
#     ----------
#     list_candidate_nodes : list
#         list of the candidate nodes to randomise
#     node2randomise_prefix : str, optional
#         prefix that identifies the nodes to randomise, by default 'random'

#     Returns
#     -------
#     list
#         list of the input nodes to randomise
#     """

#     # ensure list_candidate_nodes is unique
#     list_candidate_nodes = list(set(list_candidate_nodes))

#     # find input nodes that start with the random keyword
#     # excluding 'Group' artificial nodes
#     list_input_nodes = [
#         nd
#         for nd in list_candidate_nodes
#         if len(nd.inputs) == 0
#         and nd.name.lower().startswith(node2randomise_prefix.lower())
#         and nd.type
#         not in [
#             "GROUP_INPUT",
#             "GROUP_OUTPUT",
#         ]
#     ]

#     return list_input_nodes


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
