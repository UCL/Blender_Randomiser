import bpy


# ---------------------------
# GNGs linked to modifiers
# ---------------------------
def get_gngs_linked_to_modifiers(object):
    """Get geometry node groups that are linked to
    modifiers of the object

    NOTE: Shader node groups cannot be linked to modifiers,
    So all node groups will be geometry node groups

    Parameters
    ----------
    object : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    node_groups_linked_to_modifiers_of_object = [
        mod.node_group
        for mod in object.modifiers
        if hasattr(mod, "node_group") and hasattr(mod.node_group, "name")
    ]

    return node_groups_linked_to_modifiers_of_object


def get_modifier_linked_to_gng(gng_name, context_active_object):
    """Get the modifier of the currently active object
    linked to the input geometry node group (GNG) name

    If there are no modifiers in the currently active object
    linked to the input GNG, it will return None.

    Parameters
    ----------
    gng_name : str
        name of the GNG of interest
    context_active_object : _type_
        currently active object

    Returns
    -------
    subpanel_modifier
        modifier of the currently active object of type
        'Geometry nodes' linked to the input GNG
    """
    subpanel_modifier = None
    for mod in context_active_object.modifiers:
        if (
            hasattr(mod, "node_group")
            and (hasattr(mod.node_group, "name"))
            and (gng_name == mod.node_group.name)
        ):
            subpanel_modifier = mod
            break
    return subpanel_modifier


# ------------------------------------
# Navigating node tree of node groups
# ------------------------------------


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


# ------------------------------------
# View graph of selected node group
# ------------------------------------
def get_selectable_node_for_ng(node_group):
    """Get node associated to a (inner) geometry node group
    that allows for it to be selected

    An inner geometry node group will have a node associated with it
    in the parent node tree. That node can be selected and set as active.

    Parameters
    ----------
    geometry_node_group : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    parent_node_group = get_parent_of_ng(node_group)

    selectable_node = None
    if parent_node_group is not None:
        # get full list of nodes under the parent
        # parent can be a group node (for shader or geometry nodes)
        # or a Material (for shader nodes)
        if type(parent_node_group) != bpy.types.Material:
            list_nodes_under_parent = parent_node_group.nodes
        else:
            list_nodes_under_parent = parent_node_group.node_tree.nodes

        # get the node in the parent node_tree that wraps the node group
        # of interest
        for nd in list_nodes_under_parent:
            if (
                nd.type == "GROUP"
                and (hasattr(nd, "node_tree"))
                and (hasattr(nd.node_tree, "name"))
                and (nd.node_tree.name == node_group.name)
            ):
                selectable_node = nd
                break

    return selectable_node


def set_gngs_graph_to_top_level(root_parent_node_group):
    """Reset the geometry nodes graph view to
    the root parent geometry node group

    Parameters
    ----------
    root_parent_node_group : _type_

    """
    max_depth = get_max_depth_of_root(root_parent_node_group)
    for i in range(max_depth):
        bpy.ops.node.group_edit(exit=True)  # with exit=True we go up one level

    return
