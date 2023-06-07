import re

import bpy

from ... import utils
from ...material.property_classes.socket_properties import SocketProperties


# -----------------------------------------------------------------
# Setter / getter methods for update_sockets_collection attribute
# ----------------------------------------------------------------
def compute_UD_sockets_sets(self):
    """Compute the relevant sets of sockets for this specific
    user defined property, and add them to self.

    These sets include:
    - the set of sockets already in this GNG's collection
    - the set of sockets present in the Blender graph (for this GNG)
    - the set of sockets that are only in one of the two previous sets

    """

    # set of sockets in collection for this GNG
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )
    #####REFACTOR TO WORK WITH UI LIST/REMOVE
    # since don't need graphs for custom props?
    # set of sockets in graph for this GNG
    list_sckt_names_in_graph = [
        "UD_" + sck.name for sck in self.candidate_sockets
    ]
    self.set_sckt_names_in_graph = set(list_sckt_names_in_graph)

    # set of sockets that are just in one of the two groups
    self.set_of_sckt_names_in_one_only = (
        self.set_sckt_names_in_collection_of_props.symmetric_difference(
            self.set_sckt_names_in_graph
        )
    )


def get_update_collection(self):
    """Getter function for the update_sockets_collection attribute
    of the collection of socket properties class (ColSocketProperties)

    It will run when the property value is 'get' and
    it will update the collection of socket properties if required

    Returns
    -------
    boolean
        returns True if the collection of socket properties is updated,
        otherwise it returns False
    """
    # compute the different sets of sockets and add them to self
    compute_UD_sockets_sets(self)

    # if there is a difference between
    # sets of sockets in graph and in the collection:
    # edit the set of sockets in the collection
    if self.set_of_sckt_names_in_one_only:
        set_update_collection(self, True)
        return True
    else:
        return False


def set_update_collection(self, value):
    """
    Setter function for the update_sockets_collection attribute
    of the collection of socket properties class (ColSocketProperties)

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

    #####REFACTOR TO WORK WITH UI LIST/REMOVE
    # since don't need graphs for custom props?
    if value:
        # if the update function is triggered directly and not via
        # the getter function: compute the sets here
        if not hasattr(self, "set_of_sckt_names_in_one_only"):
            compute_UD_sockets_sets(self)

        # update the sockets that are only in either
        # the collection set or the graph
        for sckt_name in self.set_of_sckt_names_in_one_only:
            # if the socket exists only in the collection: remove from
            # collection
            if sckt_name in self.set_sckt_names_in_collection_of_props:
                self.collection.remove(self.collection.find(sckt_name))

            # if the socket exists only in the node graph: add to collection
            # with initial values
            if sckt_name in self.set_sckt_names_in_graph:
                sckt_prop = self.collection.add()
                sckt_prop.name = sckt_name
                sckt_prop.bool_randomise = True

                # TODO: review - is this code block too hacky?
                # ---------------------------------------------
                # get socket object for this socket name
                # NOTE: my definition of socket name
                # (node.name + _ + socket.name)
                for s in self.candidate_sockets:
                    # build socket id from scratch
                    socket_id = "UD_" + s.name

                    if socket_id == sckt_name:
                        sckt = s
                        break

                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]

                # extract last number between '_' and 'd/D' in the
                # attribute name, to determine the shape of the array
                # TODO: there is probably a nicer way to do this...
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dictionary with initial min/max values
                # for this socket type
                ini_min_max_values = (
                    bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                )

                # assign initial value
                for m_str in ["min", "max"]:
                    setattr(
                        sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )


# ----------------------------------------------
# ColUDSocketProperties
# ----------------------------------------------
class ColUDSocketProperties(bpy.types.PropertyGroup):
    """Class holding the collection of socket properties from
    geometry nodes and a boolean property to update the
    collection if required (for example, if new nodes are added)

    NOTE: we use the update_sockets_collection property as an
    auxiliary property because the CollectionProperty has no update function
    https://docs.blender.org/api/current/bpy.props.html#update-example

    """

    # name of the geometry node group (GNG)
    name: bpy.props.StringProperty()  # type: ignore

    # collection of socket properties for this GNG
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # helper attribute to update collection of socket properties
    update_sockets_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_collection,
        set=set_update_collection,
    )

    # candidate sockets for this GNG
    @property
    def candidate_sockets(self):  # getter method
        """Getter function for the candidate_sockets property

        We define candidate sockets as the set of output sockets
        in input nodes, in the graph for the currently active
        node group. Input nodes are nodes with only output sockets
        (i.e., no input sockets).

        It returns a list of sockets that are candidates for
        the randomisation.

        These are the output sockets of input nodes, excluding:
        - sockets of type NodeSocketGeometry (input/output nodes)
        - sockets that receive one of the available materials
          (NodeSocketMaterial)
        - sockets that receive one of the available objects
          (NodeSocketObject)
        - sockets that input a string
          (NodeSocketString)
        This is becase these sockets cannot be randomised between
        min and max values

        Returns
        -------
        list
            list of sockets in the input nodes in the graph
        """
        # get list of input nodes for this geometry node group (GNG)
        list_input_nodes = utils.get_UD_sockets_to_randomise_from_list(
            self.name
        )  #####need to get this list from UI

        # get list of sockets that are candidate for randomisation
        list_sockets = [
            out
            for nd in list_input_nodes
            for out in nd.outputs
            if type(out)
            not in [
                bpy.types.NodeSocketGeometry,
                bpy.types.NodeSocketMaterial,
                bpy.types.NodeSocketObject,
                bpy.types.NodeSocketString,
            ]
        ]  #####refactor to sockets without input nodes

        return list_sockets


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColUDSocketProperties)

    # make the property available via bpy.context.scene...
    # (i.e., bpy.context.scene.socket_props_per_gng) #####
    bpy.types.Scene.socket_props_per_UD = bpy.props.PointerProperty(
        type=ColUDSocketProperties
    )


def unregister():
    bpy.utils.unregister_class(ColUDSocketProperties)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_UD"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)
