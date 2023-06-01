import bpy


def get_parent_of_geometry_node_group(
    node_group,
):
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


def get_root_of_geometry_node_group(geometry_node_group):
    parent = get_parent_of_geometry_node_group(geometry_node_group)
    while get_parent_of_geometry_node_group(parent) is not None:
        parent = get_parent_of_geometry_node_group(parent)

    return parent


def get_inner_node_groups(
    list_candidate_root_node_groups,
):
    """Get node groups whose root parents are in
    input list

    Parameters
    ----------
    list_candidate_root_node_groups : _type_
        _description_
    """

    list_node_groups = [
        gr for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
    ]

    map_node_group_to_root_node_group = {
        gr: get_root_of_geometry_node_group(gr)
        for gr in list_node_groups
        if get_root_of_geometry_node_group(gr)
        in list_candidate_root_node_groups
    }

    return map_node_group_to_root_node_group


if __name__ == "__main__":
    # get imm parent of geoemtry node group
    list_input_nodes = [
        "Geometry Nodes",
        "NodeGroup",
        "NodeGroup.001",
        "NodeGroup.004",
    ]
    for input in list_input_nodes:
        input_node = bpy.data.node_groups[input]
        parent = get_parent_of_geometry_node_group(input_node)
        root_parent = get_root_of_geometry_node_group(input_node)

        print("---")
        if hasattr(parent, "name"):
            print(f"The parent of {input_node.name} is {parent.name}")
        else:
            print(f"The parent of {input_node.name} is {parent}")
        if hasattr(root_parent, "name"):
            print(
                f"The ROOT parent of {input_node.name} is {root_parent.name}"
            )
        else:
            print(f"The ROOT parent of {input_node.name} is {root_parent}")
        print("---")

    # get all inner nodes of a subset of nodes
    list_input_nodes = ["Geometry Nodes"]
    list_input_nodes = [bpy.data.node_groups[x] for x in list_input_nodes]
    map_node_group_to_root_node_group = get_inner_node_groups(list_input_nodes)
    print(map_node_group_to_root_node_group)
