import bpy


def get_material_input_nodes_to_randomise(
    material_str="Material", node2randomise_prefix="random"
):
    """Get list of input nodes to randomise for a given material

    Input nodes are defined as nodes with no input sockets.
    The input nodes to randomise are identified because their
    name is prefixed with node2randomise_prefix (case insensitive)

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
    list_input_nodes = [
        nd
        for nd in bpy.data.materials[material_str].node_tree.nodes
        if len(nd.inputs) == 0
        and nd.name.lower().startswith(node2randomise_prefix.lower())
    ]
    return list_input_nodes
