from random import seed, uniform

import bpy
import numpy as np
from bpy.app.handlers import persistent

from .. import config
from ..utils import node_groups as ng


# --------------------------------------------
# Operator Randomise selected sockets
# across all materials
# --------------------------------------------
class RandomiseAllMaterialNodes(bpy.types.Operator):
    """Randomise the selected output sockets
    across all materials

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
        "node.randomise_all_material_sockets"  # this is appended to bpy.ops.
    )
    bl_label = "Randomise selected sockets"
    bl_options = {"REGISTER", "UNDO"}
    testing = True

    @classmethod
    def poll(cls, context):
        # operator can only run if there are materials in the collection
        return len(context.scene.socket_props_per_material.collection) > 0

    def invoke_proxy(self, context):
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

        # add list of materials to operator self
        # (this list should have been updated already, when drawing the panel)
        cs = context.scene
        self.list_subpanel_material_names = [
            mat.name
            for mat in cs.socket_props_per_material.collection
            # for mat in cs.socket_props_per_material.candidate_materials
        ]

        # for every material: save sockets to randomise
        self.sockets_to_randomise_per_material = {}
        for mat_str in self.list_subpanel_material_names:
            # get collection of socket properties for this material
            # ATT socket properties do not include the actual socket object
            if cs.socket_props_per_material.collection[
                mat_str
            ].update_sockets_collection:
                print("Collection of material sockets updated")

            sockets_props_collection = cs.socket_props_per_material.collection[
                mat_str
            ].collection

            # get candidate sockets for this material
            candidate_sockets = cs.socket_props_per_material.collection[
                mat_str
            ].candidate_sockets

            # if socket unlinked and randomisation toggle is True:
            # modify socket props to set toggle to False
            self.sockets_to_randomise_per_material[mat_str] = []
            for sckt in candidate_sockets:
                # get socket identifier sting
                sckt_id = sckt.node.name + "_" + sckt.name
                if sckt.node.id_data.name in bpy.data.node_groups:
                    sckt_id = sckt.node.id_data.name + "_" + sckt_id

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
                        f"Socket {sckt_id} from {mat_str} is unlinked:",
                        "randomisation toggle set to False",
                    )

                # after modifying randomisation toggle
                # save list of sockets to randomise to dict,
                # with key = material
                if sockets_props_collection[sckt_id].bool_randomise:
                    self.sockets_to_randomise_per_material[mat_str].append(
                        sckt
                    )

    def invoke(self, context, event):
        self.testing = False
        self.invoke_proxy(context)

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
        if self.testing is True:
            self.invoke_proxy(context)

        cs = context.scene

        # Set the seed if it is toggled on
        previous_seed = cs.seed_properties.seed_previous
        current_seed = cs.seed_properties.seed
        seed_enabled = cs.seed_properties.seed_toggle
        if (previous_seed != current_seed) and (seed_enabled is True):
            seed(current_seed)
            cs.seed_properties.seed_previous = current_seed

        # For every material with a subpanel
        for mat_str in self.list_subpanel_material_names:
            # get collection of socket properties for this material
            # ATT socket properties do not include the actual socket object
            sockets_props_collection = cs.socket_props_per_material.collection[
                mat_str
            ].collection

            # Loop through the sockets to randomise
            for sckt in self.sockets_to_randomise_per_material[mat_str]:
                socket_id = sckt.node.name + "_" + sckt.name
                if sckt.node.id_data.name in bpy.data.node_groups:
                    socket_id = sckt.node.id_data.name + "_" + socket_id

                # min value for this socket
                min_val = np.array(
                    getattr(
                        sockets_props_collection[socket_id],
                        "min_" + cs.socket_type_to_attr[type(sckt)],
                    )
                )

                # max value for this socket
                max_val = np.array(
                    getattr(
                        sockets_props_collection[socket_id],
                        "max_" + cs.socket_type_to_attr[type(sckt)],
                    )
                )

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
                    min_val_new = np.where(min_val < max_val, min_val, max_val)

                    max_val = max_val_new
                    min_val = min_val_new

                # assign randomised socket value
                sckt.default_value = uniform(min_val, max_val)

        self.testing = True

        return {"FINISHED"}


# Without persistent, the function is removed from the handlers' list
#  once executed
@persistent
def randomise_material_nodes_per_frame(dummy):
    bpy.ops.node.randomise_all_material_sockets("INVOKE_DEFAULT")

    return


# -------------------------------
# Operator: view graph for material
# -------------------------------
class ViewNodeGraphOneMaterial(bpy.types.Operator):
    """Show node graph for the material

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
        "node.view_graph"  # this is appended to bpy.ops.
        # NOTE: it will be overwritten
    )
    bl_label = "View node graph for this material"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        """Determine whether the operator can be executed

        The name of the subpanel must be a material in Blender's data
        structure

        If the operator can't be executed, the button will appear as disabled.

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        # used to check if the operator can run.
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.collection[
            cls.subpanel_material_idx
        ]

        # e.g: cls.subpanel_material_name = subpanel_material.name
        return subpanel_material.name in [
            mat.name for mat in bpy.data.materials
        ]

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
        # add list of socket properties to operator self
        # (this list should have been updated already, when drawing the panel)
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.collection[
            self.subpanel_material_idx
        ]
        self.subpanel_material_name = subpanel_material.name

        return self.execute(context)

    def execute(self, context):
        """Execute 'view graph' operator

        Show the node graph for this material.

        We change the view by changing the 'slot'. If we change the
        active material only, the slot in view is 'overwritten' with
        the active material every time.

        It may be the case that a material is not assigned to any slot.
        In that case, if the view-graph button is clicked, a new
        slot is added for that material.

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        cob = context.object

        # get the subpanel's material slot index
        # returns -1 if there is no slot for that material
        slot_idx_for_subpanel_material = cob.material_slots.find(
            self.subpanel_material_name
        )

        # change active slot shown in graph
        # NOTE: switching slot switches the active material too
        if (
            slot_idx_for_subpanel_material == -1
        ):  # if no slot for this material
            bpy.ops.object.material_slot_add()  # add a new slot
            cob.active_material_index = len(cob.material_slots) - 1
        else:
            cob.active_material_index = slot_idx_for_subpanel_material

        # check if the subpanel's material is the active one
        # (when I switch slot the material switches too)
        if (
            bpy.data.materials[self.subpanel_material_name]
            != cob.active_material
        ):
            cob.active_material = bpy.data.materials[
                self.subpanel_material_name
            ]

        # ensure we are at the top level in the graph
        ng.set_ngs_graph_to_top_level(
            bpy.data.materials[self.subpanel_material_name]
        )

        return {"FINISHED"}


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [RandomiseAllMaterialNodes]


for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    operator_i = type(
        f"ViewNodeGraphOneMaterial_subpanel_{i}",
        (
            ViewNodeGraphOneMaterial,
            bpy.types.Operator,
        ),
        {
            "bl_idname": f"node.view_graph_for_material_{i}",
            "bl_label": "",
            "subpanel_material_idx": i,
        },
    )
    list_classes_to_register.append(operator_i)  # type: ignore


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(
        randomise_material_nodes_per_frame
    )

    print("material operators registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(
        randomise_material_nodes_per_frame
    )

    print("material operators unregistered")
