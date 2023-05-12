import bpy

from ..material.property_classes.socket_properties import SocketProperties

# -----------------------
# SocketProperties
# ---------------------
# Should work as is?


# ----------------------------------------------
# ColGeomSocketProperties
# ----------------------------------------------
class ColGeomSocketProperties(bpy.types.PropertyGroup):
    """Class holding the collection of socket properties from
    **geometry** nodes and a boolean property to update the
    collection if required (for example, if new nodes are added)

    NOTE: we use the update_sockets_collection property as an
    auxiliary property because the CollectionProperty has no update function
    https://docs.blender.org/api/current/bpy.props.html#update-example

    """

    # name of the node group
    name: bpy.props.StringProperty()  # type: ignore

    # collection of socket properties
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # 'dummy' attribute to update collection of socket properties
    update_sockets_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        # get=get_update_collection,-------------
        # set=set_update_collection, ------------
    )

    # candidate sockets for this node group
    @property
    def candidate_sockets(self):  # getter method
        """Get function for the candidate_sockets property

        We define candidate sockets as the set of output sockets
        in input nodes, in the graph for the currently active
        material. Input nodes are nodes with only output sockets
        (i.e., no input sockets).

        It returns a list of sockets that are candidates for
        the randomisation.


        Returns
        -------
        list
            list of sockets in the input nodes in the graph
        """
        # get list of input nodes for this material
        # input nodes are defined as those:
        # - with no input sockets
        # - their name starts with random
        # - and they can be independent or
        # inside a node group #---- I think I can change this
        # list_input_nodes = utils.get_material_nodes_to_randomise_all(
        # self.name)
        # #---- instead: get for this node group

        # # list of sockets
        # list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
        list_sockets = ["a", "b", "c"]

        return list_sockets


# ---------------------------------------------------
# Collection of Geometry Node groups (ColMaterials)
# ---------------------------------------------------
class ColGeomNodeGroups(bpy.types.PropertyGroup):
    # collection of [collections of socket properties] (one per node group)
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=ColGeomSocketProperties
    )

    # autopopulate collection of geometry node groups
    update_materials_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        # get=get_update_materials_collection, ----------
        # set=set_update_materials_collection, --------------
    )

    # candidate geometry node groups
    @property
    def candidate_geom_node_groups(self):  # getter method
        # self is the collection of node groups
        list_node_groups = [
            nd.name for nd in bpy.data.node_groups if nd.type == "GEOMETRY"
        ]
        return list_node_groups


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
list_classes_to_register = [ColGeomSocketProperties, ColGeomNodeGroups]


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    # make available via bpy.context.scene...
    bprop = bpy.props
    bpy.types.Scene.socket_props_per_geom_nodegroup = bprop.PointerProperty(
        type=ColGeomNodeGroups
    )

    print("geometry properties registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_geom_nodegroup"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)

    print("geometry properties unregistered")
