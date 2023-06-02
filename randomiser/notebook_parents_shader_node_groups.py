import bpy


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
    # initialise parent of the shader node group
    parent_sng = None

    # check if parent is a shader node group
    list_all_sngs = [gr for gr in bpy.data.node_groups if gr.type == "SHADER"]
    for gr in list_all_sngs:
        for nd in gr.nodes:
            if (
                (hasattr(nd, "node_tree"))
                and (hasattr(nd.node_tree, "name"))
                and (nd.node_tree.name == node_group.name)
            ):
                parent_sng = gr
                break

    # check if parent is a material
    list_all_materials = [mat for mat in bpy.data.materials if mat.use_nodes]
    # TODO: is it possible that a material has no node_tree?
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


# get root parent of shader node group
def get_root_of_sng(shader_node_group):
    """Get root parent of input shader node group

    It returns the root parent (i.e., the parent node group whose
    parent is None), for the input geometry node group

    Parameters
    ----------
    geometry_node_group : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    parent = get_parent_of_sng(shader_node_group)
    c = 1  # TODO: should this be 0? ---double check
    while get_parent_of_sng(parent) is not None:
        c += 1
        parent = get_parent_of_sng(parent)

    return (parent, c)


if __name__ == "__main__":
    # print immediate parent
    list_node_groups_names = [
        "NodeGroup",
        "NodeGroup.001",
        "NodeGroup.002",
        "NodeGroup.003",
    ]
    for gr_str in list_node_groups_names:
        parent_node = get_parent_of_sng(bpy.data.node_groups[gr_str])
        print(parent_node)
