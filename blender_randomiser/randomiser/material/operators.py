import bpy
import numpy as np


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
        # add list of socket properties to operator self
        # TODO: do I need to update it here?
        # (I think I dont because it is updated when drawing the panel,
        # which happens before this)
        cs = context.scene
        self.sockets_props_collection = cs.sockets2randomise_props.collection

        # if socket unlinked and toggle is true: set toggle to false
        for sckt in cs.candidate_sockets:
            sckt_id = sckt.node.name + "_" + sckt.name
            if (not sckt.is_linked) and (
                self.sockets_props_collection[sckt_id].bool_randomise
            ):
                setattr(
                    self.sockets_props_collection[sckt_id],
                    "bool_randomise",
                    False,
                )
                print(
                    f"Socket {sckt_id} unlinked:",
                    "randomisation toggle set to False",
                )

        # add list sockets to randomise to self.
        self.list_sockets_to_randomise = [
            sckt
            for sckt in cs.candidate_sockets
            if self.sockets_props_collection[
                sckt.node.name + "_" + sckt.name
            ].bool_randomise
        ]

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

        # Loop thru sockets to randomise
        for sckt in self.list_sockets_to_randomise:
            socket_id = sckt.node.name + "_" + sckt.name

            # min value for this socket
            min_val = np.array(
                getattr(
                    self.sockets_props_collection[socket_id],
                    "min_" + context.scene.socket_type_to_attr[type(sckt)],
                )
            )

            # max value for this socket
            max_val = np.array(
                getattr(
                    self.sockets_props_collection[socket_id],
                    "max_" + context.scene.socket_type_to_attr[type(sckt)],
                )
            )

            # if type of the socket is color, and max_val < min_val:
            # switch them before randomising
            # NOTE: these are not switched in the display panel
            # (this is intended)
            if (type(sckt) == bpy.types.NodeSocketColor) and any(
                max_val < min_val
            ):
                max_val_new = np.where(max_val >= min_val, max_val, min_val)
                min_val_new = np.where(min_val < max_val, min_val, max_val)

                # TODO: is there a more elegant way?
                # feels a bit clunky....
                max_val = max_val_new
                min_val = min_val_new

            # assign randomised socket value between min and max
            sckt.default_value = rng.uniform(low=min_val, high=max_val)

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
    print("material operators unregistered")
