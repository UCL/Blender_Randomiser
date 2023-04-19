import re

import bpy

from .socket_properties import SocketProperties


# ----------------------------------------------------
# Setter / getter methods for update_collection attribute
# -----------------------------------------------------
def set_update_collection(self, value):
    """
    'Set' function for the update_sockets_collection attribute
    of the class ColSocketProperties.

    It will run when the property value is 'set'.

    It will update the collection of socket properties as follows:
        - For the set of sockets that exist only in either
        the collection or the graph:
            - if the socket exists only in the collection: remove from
            collection
            - if the socket exists only in the node graph: add to collection
            with initial values
        - For the rest of sockets: leave untouched

    Parameters
    ----------
    value : boolean
        if True, the collection of socket properties is
        overwritten to consider the latest data
    """

    if value:
        # update sockets that are only in either
        # the collection set or the graph set
        for sckt_name in self.set_of_sckt_names_in_one_only:
            # - if the socket exists only in the collection: remove from
            # collection
            if sckt_name in self.set_sckt_names_in_collection_of_props:
                self.collection.remove(self.collection.find(sckt_name))

            # - if the socket exists only in the node graph: add to collection
            # with initial values
            if sckt_name in self.set_sckt_names_in_graph:
                sckt_prop = self.collection.add()
                sckt_prop.name = sckt_name
                sckt_prop.bool_randomise = True

                # ---------------------------
                # get socket object for this socket name
                # NOTE: my definition of socket name
                # (node.name + _ + socket.name)
                sckt = [
                    s
                    for s in self.candidate_sockets
                    if s.node.name + "_" + s.name == sckt_name
                ][0]

                # add min/max values
                # TODO: review - is this too hacky?
                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]
                # for the shape of the array from the attribute name:
                # extract last number between '_' and 'd/D' in the attribute
                # name
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dict with initial min/max values for this socket type
                ini_min_max_values = (
                    bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                )

                # assign initial value ----only if
                for m_str in ["min", "max"]:
                    setattr(
                        sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )


def get_update_collection(self):
    """Get function for the update_sockets_collection attribute
    of the class ColSocketProperties

    It will run when the property value is 'get' and
    it will update the collection of socket properties if required

    Returns
    -------
    boolean
        returns True if the collection of socket properties is updated,
        otherwise it returns False
    """

    # set of sockets in collection for this material
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # set of sockets in graph *for this material* !
    self.set_sckt_names_in_graph = set(
        sck.node.name + "_" + sck.name for sck in self.candidate_sockets
    )

    # set of sockets that are just in one of the two groups
    self.set_of_sckt_names_in_one_only = (
        self.set_sckt_names_in_collection_of_props.symmetric_difference(
            self.set_sckt_names_in_graph
        )
    )

    # if there is a difference:
    # edit the set of sockets in collection
    # for this material with the latest data
    if self.set_of_sckt_names_in_one_only:
        set_update_collection(self, True)
        return True  # if returns True, it has been updated
    else:
        return False  # if returns False, it hasn't


# -----------------------
# ColSocketProperties
# ---------------------
class ColSocketProperties(bpy.types.PropertyGroup):
    """Class holding the collection of socket properties and
    a boolean property to update the collection if required
    (for example, if new nodes are added)

    NOTE: we use the update_sockets_collection property as an
    auxiliary property because the CollectionProperty has no update function
    https://docs.blender.org/api/current/bpy.props.html#update-example

    """

    # name of the material
    name: bpy.props.StringProperty()  # type: ignore

    # collection of socket properties
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # 'dummy' attribute to update collection of socket properties
    update_sockets_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_collection,
        set=set_update_collection,
    )

    # --------------------------------
    # candidate sockets for this material
    # TODO : can I use decorator instead?
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
        list_input_nodes = [
            nd
            for nd in bpy.data.materials[self.name].node_tree.nodes
            if len(nd.inputs) == 0
            and nd.name.lower().startswith("random".lower())
        ]

        # list of sockets
        # TODO: should we exclude unlinked ones here instead?
        list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
        return list_sockets

    # ---------------


def register():
    bpy.utils.register_class(ColSocketProperties)

    # make available via bpy.context.scene...
    bpy.types.Scene.socket_props_per_material = bpy.props.CollectionProperty(
        type=ColSocketProperties
    )


def unregister():
    bpy.utils.unregister_class(ColSocketProperties)

    # remove from bpy.context.scene...
    if hasattr(bpy.types.Scene, "socket_props_per_material"):
        delattr(bpy.types.Scene, "socket_props_per_material")
