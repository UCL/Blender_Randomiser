import bpy

from . import config


def get_UD_sockets_to_randomise_from_list(
    list_candidate_nodes: list,
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
        # if len(nd.inputs) == 0
        # and nd.name.lower().startswith(node2randomise_prefix.lower())
        # and nd.type
        # not in [
        #     "GROUP_INPUT",
        #     "GROUP_OUTPUT",
        # ]
    ]

    return list_input_nodes


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
    # find input nodes that start with random
    # excluding 'Group Inpuyt/Output' nodes,
    # and any nested Group nodes
    # NOTE: nested Group nodes are included in bpy.data.node_groups
    # of type 'GEOMETRY'
    list_input_nodes = get_nodes_to_randomise_from_list(
        [
            nd
            for nd in bpy.data.node_groups[node_group_str].nodes
            if nd.type != "GROUP"  # exclude groups inside of groups
        ],
        node2randomise_prefix,
    )

    return list_input_nodes


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

    list_all_gngs = [
        gr for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
    ]

    parent_gng = None
    if node_group is not None:
        for gr in list_all_gngs:
            for nd in gr.nodes:
                if (
                    (hasattr(nd, "node_tree"))
                    and (hasattr(nd.node_tree, "name"))
                    and (nd.node_tree.name == node_group.name)
                ):
                    parent_gng = gr
                    break

    return parent_gng  # immediate parent


def get_root_of_gng(geometry_node_group):
    """Get root parent of input geometry node group

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
    parent = get_parent_of_gng(geometry_node_group)
    c = 1  # TODO: should this be 0?
    while get_parent_of_gng(parent) is not None:
        c += 1
        parent = get_parent_of_gng(parent)

    return (parent, c)


def get_map_inner_gngs(
    list_candidate_root_node_groups,
):
    """Compute dictionary that maps inner node groups of the
    input root parent node groups, to a tuple made of
    - the inner node group's root parent node group,
    - the inner node group's depth

    The dictionary is computed for inner node groups whose root parents
    are in the input list

    Parameters
    ----------
    list_candidate_root_node_groups : _type_
        _description_
    """

    list_node_groups = [
        gr for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
    ]

    map_node_group_to_root_node_group = {
        gr: get_root_of_gng(gr)  # tuple
        for gr in list_node_groups
        if get_root_of_gng(gr)[0] in list_candidate_root_node_groups
    }

    return map_node_group_to_root_node_group


def get_selectable_node_for_node_group(geometry_node_group):
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
    parent_node_group = get_parent_of_gng(geometry_node_group)

    selectable_node = None
    if parent_node_group is not None:
        for nd in parent_node_group.nodes:
            if (
                nd.type == "GROUP"
                and (hasattr(nd, "node_tree"))
                and (hasattr(nd.node_tree, "name"))
                and (nd.node_tree.name == geometry_node_group.name)
            ):
                selectable_node = nd
                break

    return selectable_node


def get_path_to_gng(gng):
    """Compute path of parent geometry group nodes up
    to the input geometry group node

    Both the root parent node group and the input
    geometry group node are included

    Parameters
    ----------
    gng : _type_
        inner geometry group need of which we want to
        obtain the path

    Returns
    -------
    path_to_gng: list
        a list of parent geometry group nodes up to the input one
    """

    parent = get_parent_of_gng(gng)
    if parent is None:
        path_to_gng = []
    else:
        path_to_gng = [parent]
        while get_parent_of_gng(parent) is not None:
            parent = get_parent_of_gng(parent)
            path_to_gng.append(parent)

        path_to_gng.reverse()

    path_to_gng.append(gng)
    return path_to_gng


def get_max_depth(root_parent_node_group):
    """Compute the maximum depth of any inner geometry group
    for the given root parent node group

    A root parent node group is a node group whose parent is
    None

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
    map_inner_gngs_of_modifier = get_map_inner_gngs([root_parent_node_group])
    max_depth = 0
    if map_inner_gngs_of_modifier:
        max_depth = max([v[1] for k, v in map_inner_gngs_of_modifier.items()])

    return max_depth


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


def set_gngs_graph_to_top_level(root_parent_node_group):
    """Reset the geometry nodes graph view to
    the root parent geometry node group

    Parameters
    ----------
    root_parent_node_group : _type_

    """
    max_depth = get_max_depth(root_parent_node_group)
    for i in range(max_depth):
        bpy.ops.node.group_edit(exit=True)  # with exit=True we go up one level

    return
