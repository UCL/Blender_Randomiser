import re

import bpy

from ...material.property_classes.socket_properties import SocketProperties
from ...utils import nodes2rand as nr


# -----------------------------------------------------------------
# Setter / getter methods for update_sockets_collection attribute
# ----------------------------------------------------------------
def compute_geom_sockets_sets(self):
    """Compute the relevant sets of sockets for this specific
    Geometry Node Group, and add them to self.

    These sets include:
    - the set of sockets already in this GNG's collection
    - the set of sockets present in the Blender graph (for this GNG)
    - the set of sockets that are only in one of the two previous sets

    """

    # set of sockets in collection for this GNG
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # set of sockets in graph for this GNG
    list_sckt_names_in_graph = [
        sck.node.name + "_" + sck.name for sck in self.candidate_sockets
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
    compute_geom_sockets_sets(self)

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

    if value:
        # if the update function is triggered directly and not via
        # the getter function: compute the sets here
        if not hasattr(self, "set_of_sckt_names_in_one_only"):
            compute_geom_sockets_sets(self)

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
                    socket_id = s.node.name + "_" + s.name

                    if socket_id == sckt_name:
                        sckt = s
                        break

                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]

                print("type(sckt) = ", type(sckt))

                # extract last number between '_' and 'd/D' in the
                # attribute name, to determine the shape of the array
                # TODO: there is probably a nicer way to do this...
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dictionary with initial min/max values
                # for this socket type

                # sckt_prop.input_json = True

                # if sckt_prop.input_json:
                #     print("sckt_prop.input_json is True")
                #     ini_min_max_values = (
                #         bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                #     )
                # else:
                #     print("sckt_prop.input_json is False")
                #     ini_min_max_values = (
                #         bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                #     )

                if self.input_json:
                    print("Initial values have already been set by .json")

                else:
                    print("input_json is False")
                    ini_min_max_values = (
                        bpy.context.scene.socket_type_to_ini_min_max[
                            type(sckt)
                        ]
                    )

                    # assign initial value
                    for m_str in ["min", "max"]:
                        setattr(
                            sckt_prop,
                            m_str + "_" + socket_attrib_str,
                            (ini_min_max_values[m_str],) * n_dim,
                        )
                    print("ASSIGNMENTS ========= ")
                    print(ini_min_max_values)
                    print(sckt_prop)
                    print(socket_attrib_str)


def get_input_json(self):
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
    # if there is a difference between
    # sets of sockets in graph and in the collection:
    # edit the set of sockets in the collection
    if self.input_json:
        set_input_json(self, True)
        return True
    else:
        return False


def set_input_json(self, value):
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

    if value:
        print("if value is True")
        self.input_json = True
    else:
        print("else value is false")
        self.input_json = False

    print(self.input_json)


# ----------------------------------------------
# ColGeomSocketProperties
# ----------------------------------------------
class ColGeomSocketProperties(bpy.types.PropertyGroup):
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

    input_json: bpy.props.BoolProperty(  # type: ignore
        default=False,
    )

    update_input_json: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_input_json,
        set=set_input_json,
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
        list_input_nodes = nr.get_geometry_nodes_to_randomise(self.name)

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
        ]

        return list_sockets


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColGeomSocketProperties)


def unregister():
    bpy.utils.unregister_class(ColGeomSocketProperties)
