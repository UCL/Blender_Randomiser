import bpy


def get_material_input_nodes_to_randomise(
    material_str="Material", node2randomise_prefix="random"
):
    """Get list of input nodes to randomise for a given material.

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

    # list of nodes for current material
    # split into those belonging to a group or not
    list_material_nodes_indep = []
    list_material_nodes_in_groups = []
    for nd in bpy.data.materials[material_str].node_tree.nodes:
        if nd.type != "GROUP":
            list_material_nodes_indep.append(nd)  # 'independent' nodes
        else:
            list_material_nodes_in_groups.extend(
                nd.node_tree.nodes
            )  # nodes inside groups

    # ensure list_material_nodes_in_groups is unique
    # TODO: what if two groups have a node with the same name??
    # --it will work if nodegroups have different names!
    # maybe assume geometry node groups will start/end with Geometry?
    list_material_nodes_in_groups = list(set(list_material_nodes_in_groups))

    # find input nodes that startwith random
    # in any of those groups
    # excluding 'Group' nodes
    list_input_nodes = [
        nd
        for nd in list_material_nodes_indep + list_material_nodes_in_groups
        if len(nd.inputs) == 0
        and nd.name.lower().startswith(node2randomise_prefix.lower())
        and nd.type
        not in [
            "GROUP_INPUT",
            "GROUP_OUTPUT",
        ]  # exclude 'Group' artificial nodes
    ]

    return list_input_nodes
