import bpy

from ...material.property_classes.socket_properties import SocketProperties

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
        # get=get_update_collection,<-------------
        # set=set_update_collection, <------------
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


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColGeomSocketProperties)


def unregister():
    bpy.utils.unregister_class(ColGeomSocketProperties)
