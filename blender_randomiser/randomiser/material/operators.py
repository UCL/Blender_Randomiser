import bpy
import numpy as np

from .. import utils


# -------------------------------
## Operators
class RandomiseMaterialNodes(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise the selected output sockets

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # operator metadata
    bl_idname = "node.randomise_socket"  # this is appended to bpy.ops.
    bl_label = "Randomise selected sockets from input material nodes"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current (object) context
    # NOTE: but it actually checks if there is an object in this context right?
    @classmethod
    def poll(cls, context):
        return context.object is not None

    # ------------------------------

    def invoke(self, context, event):
        """Initialise parmeters before executing

        The invoke() function runs before executing the operator.
        Here, we
        - add the list of input nodes and collection of socket propertiess to
          the operator self,
        - unselect the randomisation toggle of the sockets of input nodes if
          they are not linked to any other node

        Parameters
        ----------
        context : bpy_types.Context
            the context from which the operator is executed
        event : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        # add list of input nodes to operator self
        self.list_input_nodes = utils.get_material_input_nodes_to_randomise()

        # add list of socket properties to operator self
        # TODO: do I need to update it here?
        # (I think I dont because it is updated when drawing the panel,
        # which happens before this)
        # --------------
        self.sockets_props_collection = context.scene.sockets2randomise_props

        # if socket unlinked and toggle is true: set toggle to false
        for nd in self.list_input_nodes:
            for out in nd.outputs:
                sckt_id = nd.name + "_" + out.name
                if (not out.is_linked) and (
                    self.sockets_props_collection[sckt_id].bool_randomise
                ):
                    setattr(
                        self.sockets_props_collection[sckt_id],
                        "bool_randomise",
                        False,
                    )

        return self.execute(context)

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        """Execute the randomiser operator

        Randomise the selected output sockets between
        the min/max values provided

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        # Construct a numpy random number generator
        rng = np.random.default_rng()

        # Loop thru input nodes and their selected output sockets
        # to assign to each a uniformly sampled value btw min and max
        for nd in self.list_input_nodes:
            # get list of selected sockets for this node
            list_sockets_to_randomise = [
                sck
                for sck in nd.outputs
                if (
                    self.sockets_props_collection[
                        nd.name + "_" + sck.name
                    ].bool_randomise
                )
            ]

            # randomise their value
            for out in list_sockets_to_randomise:
                socket_id = nd.name + "_" + out.name

                # min value for this socket
                min_val = np.array(
                    getattr(
                        self.sockets_props_collection[socket_id],
                        "min_" + context.scene.socket_type_to_attr[type(out)],
                    )
                )

                # max value for this socket
                max_val = np.array(
                    getattr(
                        self.sockets_props_collection[socket_id],
                        "max_" + context.scene.socket_type_to_attr[type(out)],
                    )
                )

                # if type of the socket is color, and max_val < min_val:
                # switch them before randomising
                # NOTE: these are not switched in the display panel
                # (this is intended)
                if (type(out) == bpy.types.NodeSocketColor) and any(
                    max_val < min_val
                ):
                    max_val_new = np.where(
                        max_val >= min_val, max_val, min_val
                    )
                    min_val_new = np.where(min_val < max_val, min_val, max_val)

                    # TODO: is there a more elegant way?
                    # feels a bit clunky....
                    max_val = max_val_new
                    min_val = min_val_new

                # assign randomised socket value between min and max
                out.default_value = rng.uniform(low=min_val, high=max_val)

        return {"FINISHED"}


# -------------------------------
## Register operators

list_classes_to_register = [
    RandomiseMaterialNodes,
]


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("material operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material opertors unregistered")
