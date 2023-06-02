import bpy


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


def get_root_and_depth_of_ng(node_group):
    # select function to compute parent of node group
    # based on node group type
    # TODO: combine this with path?
    if node_group.type == "SHADER" or type(node_group) == bpy.types.Material:
        get_parent_of_ng = get_parent_of_sng
    elif node_group.type == "GEOMETRY":
        get_parent_of_ng = get_parent_of_gng

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


if __name__ == "__main__":
    map = get_map_inner_ngs_given_roots([bpy.data.materials["Material"]])
    list_inner_node_groups = list(map.keys())
    print(list_inner_node_groups)
