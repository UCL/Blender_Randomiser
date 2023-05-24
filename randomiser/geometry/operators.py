import random

import bpy
import numpy as np
from bpy.app.handlers import persistent


# --------------------------------------------
# Operator Randomise selected sockets
# across all Geometry node groups
# --------------------------------------------
class RandomiseAllGeometryNodes(bpy.types.Operator):
    """Randomise the selected output sockets
    across all geometry node groups

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # metadata
    bl_idname = (
        "node.randomise_all_geometry_sockets"  # this is appended to bpy.ops.
    )
    bl_label = "Randomise selected sockets"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # operator can only run if there are geometry node groups
        # in the collection
        return len(context.scene.socket_props_per_gng.collection) > 0

    def invoke(self, context, event):
        """Initialise parmeters before executing

        The invoke() function runs before executing the operator.
        Here, we
        - add the list of input nodes and collection of socket properties to
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
        # add list of GNGs to operator self
        # (this list should have been updated already, when drawing the panel)
        cs = context.scene
        self.list_subpanel_gng_names = [
            gng.name for gng in cs.socket_props_per_gng.collection
        ]

        # for every GNG: save sockets to randomise
        self.sockets_to_randomise_per_gng = {}
        for gng_str in self.list_subpanel_gng_names:
            # get collection of socket properties for this GNG
            # ATT socket properties do not include the actual socket object
            if cs.socket_props_per_gng.collection[
                gng_str
            ].update_sockets_collection:
                print("Collection of geometry sockets updated")

            sockets_props_collection = cs.socket_props_per_gng.collection[
                gng_str
            ].collection

            # get candidate sockets for this GNG
            candidate_sockets = cs.socket_props_per_gng.collection[
                gng_str
            ].candidate_sockets

            # if socket unlinked and randomisation toggle is True:
            # modify socket props to set toggle to False
            self.sockets_to_randomise_per_gng[gng_str] = []
            for sckt in candidate_sockets:
                # get socket identifier string
                sckt_id = sckt.node.name + "_" + sckt.name

                # if (sckt.node.id_data.name in bpy.data.node_groups) and (
                #     bpy.data.node_groups[sckt.node.id_data.name].type
                # != "GEOMETRY"
                # ):  # only for SHADER groups
                #     sckt_id = sckt.node.id_data.name + "_" + sckt_id

                # if this socket is selected to randomise but it is unlinked:
                # set randomisation toggle to False
                if (not sckt.is_linked) and (
                    sockets_props_collection[sckt_id].bool_randomise
                ):
                    setattr(
                        sockets_props_collection[sckt_id],
                        "bool_randomise",
                        False,
                    )
                    print(
                        f"Socket {sckt_id} from {gng_str} is unlinked:",
                        "randomisation toggle set to False",
                    )

                # after modifying randomisation toggle
                # save list of sockets to randomise to dict,
                # with key = material
                if sockets_props_collection[sckt_id].bool_randomise:
                    self.sockets_to_randomise_per_gng[gng_str].append(sckt)

        return self.execute(context)

    def execute(self, context):
        """Execute the randomiser operator

        Randomise the selected output sockets between
        their min and max values.

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        cs = context.scene

        # Construct a numpy random number generator
        # rng = np.random.default_rng()

        # For every GNG with a subpanel
        for gng_str in self.list_subpanel_gng_names:
            # get collection of socket properties for this material
            # ATT socket properties do not include the actual socket object
            sockets_props_collection = cs.socket_props_per_gng.collection[
                gng_str
            ].collection

            # Loop through the sockets to randomise
            for sckt in self.sockets_to_randomise_per_gng[gng_str]:
                socket_id = sckt.node.name + "_" + sckt.name

                # get min value for this socket
                min_val = np.array(
                    getattr(
                        sockets_props_collection[socket_id],
                        "min_" + cs.socket_type_to_attr[type(sckt)],
                    )
                )

                # get max value for this socket
                max_val = np.array(
                    getattr(
                        sockets_props_collection[socket_id],
                        "max_" + cs.socket_type_to_attr[type(sckt)],
                    )
                )

                # if socket type is boolean
                if type(sckt) == bpy.types.NodeSocketBool:
                    sckt.default_value = random.choice([True, False])
                    # Faster: bool(random.getrandbits(1))F
                    # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python

                # if socket type is int
                elif type(sckt) == bpy.types.NodeSocketInt:
                    sckt.default_value = random.randint(max_val, min_val)

                # for all other socket types
                else:
                    # if type of the socket is NodeSocketColor,
                    # and max_val < min_val:
                    # switch them before randomising
                    # NOTE: these are not switched in the display panel
                    # (this is intended)
                    if (type(sckt) == bpy.types.NodeSocketColor) and any(
                        max_val < min_val
                    ):
                        max_val_new = np.where(
                            max_val >= min_val, max_val, min_val
                        )
                        min_val_new = np.where(
                            min_val < max_val, min_val, max_val
                        )

                        # TODO: is there a more elegant way?
                        # feels a bit clunky....
                        max_val = max_val_new
                        min_val = min_val_new

                    # assign randomised socket value
                    # print(random.uniform(min_val, max_val))
                    sckt.default_value = random.uniform(min_val, max_val)

        return {"FINISHED"}


# Without persistent, the function is removed from the handlers' list
#  once executed
@persistent
def randomise_geometry_nodes_per_frame(dummy):
    bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")

    return


# -------------------------------
# Operator: view graph per GNG
# -------------------------------


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [RandomiseAllGeometryNodes]

# one view graph operator per nodegroup!


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(
        randomise_geometry_nodes_per_frame
    )

    print("geometry operators registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(
        randomise_geometry_nodes_per_frame
    )

    print("geometry operators unregistered")
    print("geometry operators unregistered")
