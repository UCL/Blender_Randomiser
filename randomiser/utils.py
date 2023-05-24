import bpy

from . import config


def get_nodes_to_randomise_from_list(
    list_candidate_nodes: list,
    node2randomise_prefix: str = config.DEFAULT_RANDOM_KEYWORD,
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
    # TODO: what if two groups have a node with the same name??
    # --it will work if nodegroups have different names!
    # maybe assume geometry node groups will start/end with Geometry?
    list_candidate_nodes = list(set(list_candidate_nodes))

    # find input nodes that startwith random
    # in any of those groups
    # excluding 'Group' nodes
    list_input_nodes = [
        nd
        for nd in list_candidate_nodes
        if len(nd.inputs) == 0
        and nd.name.lower().startswith(node2randomise_prefix.lower())
        and nd.type
        not in [
            "GROUP_INPUT",
            "GROUP_OUTPUT",
        ]  # exclude 'Group' artificial nodes
    ]

    return list_input_nodes


def get_material_nodes_to_randomise_indep(
    material_str: str = "Material",
    node2randomise_prefix: str = config.DEFAULT_RANDOM_KEYWORD,
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


def get_material_nodes_to_randomise_group(
    material_str: str = "Material",
    node2randomise_prefix: str = config.DEFAULT_RANDOM_KEYWORD,
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
    # belonging to a group
    list_material_nodes_in_groups = []
    for nd in bpy.data.materials[material_str].node_tree.nodes:
        if nd.type == "GROUP":
            list_material_nodes_in_groups.extend(
                nd.node_tree.nodes
            )  # nodes inside groups

    # find input nodes that startwith random
    # in any of those groups
    # excluding 'Group' nodes
    list_input_nodes = get_nodes_to_randomise_from_list(
        list_material_nodes_in_groups
    )

    return list_input_nodes


def get_material_nodes_to_randomise_all(
    material_str: str = "Material",
    node2randomise_prefix: str = config.DEFAULT_RANDOM_KEYWORD,
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


def get_geometry_nodes_to_randomise(
    node_group_str: str = "Geometry Nodes",
    node2randomise_prefix: str = config.DEFAULT_RANDOM_KEYWORD,
):
    # find input nodes that startwith random
    # excluding 'Group Inpuyt/Output' nodes,
    # and any nested Group nodes! (these are included in bpy.data.node_groups
    # of type 'GEOMETRY')
    list_input_nodes = get_nodes_to_randomise_from_list(
        [
            nd
            for nd in bpy.data.node_groups[node_group_str].nodes
            if nd.type != "GROUP"  # exclude groups inside of groups
        ],
        node2randomise_prefix,
    )

    return list_input_nodes
