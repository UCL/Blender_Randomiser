import random

import bpy
import numpy as np
from bpy.app.handlers import persistent

from .. import config


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
                    sckt.default_value = random.choice(
                        [bool(list(m_val)[0]) for m_val in [min_val, max_val]]
                    )  # 1d only
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
class ViewNodeGraphOneGNG(bpy.types.Operator):
    """Show node graph for the Geometry Node Group

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
        "gng.view_graph"  # this is appended to bpy.ops.
        # NOTE: it will be overwritten
    )
    bl_label = "View node graph for this Geometry node group"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # used to check if the operator can run.
        # the geometry is linked to a specific object...
        # so only node groups relevant to a specific object should show?
        cs = context.scene
        subpanel_gng = cs.socket_props_per_gng.collection[cls.subpanel_gng_idx]

        # the GNG must be a Geometry node group
        return subpanel_gng.name in [
            gr.name for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
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
        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]
        self.subpanel_gng_name = subpanel_gng.name

        return self.execute(context)

    def execute(self, context):
        """Execute 'view graph' operator

        It shows the node graph for the geometry node group.

        In practice, we change the graph view by changing the active modifier.
        This implies that a geometry node tree is linked to a modifier.

        It may be the case that a geometry node tree is not assigned
        to any modifier. In that case, if the view-graph button is clicked,
        a new modifier is added for that geometry node tree.

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

        # find the modifier linked to this GNG
        # mod.node_group => node group linked to the modifier
        # a modifier may be linkable to a GNG or not!
        # (it may not have node_group attr)
        subpanel_modifier = ""
        for mod in cob.modifiers:
            if (
                hasattr(mod, "node_group")
                and (hasattr(mod.node_group, "name"))
                and (self.subpanel_gng_name == mod.node_group.name)
            ):
                subpanel_modifier = mod
                break

        # if there is a modifier linked to this GNG: set that
        # modifier as active (this will change the displayed graph)
        # TODO: else: assign to a modifier
        if subpanel_modifier:
            bpy.ops.object.modifier_set_active(modifier=subpanel_modifier.name)

        # if there is no modifier linked to this GNG and
        # is a Geometry node tree
        # Q: does this only happen if the node group is
        # not a geometry node tree?
        # (can I have a geometry node tree that is not linked to a modifier?)
        # ---yes, for example when you unlink or make a copy
        else:
            # create a new modifier with a new geometry node group
            bpy.ops.node.new_geometry_nodes_modifier()  # will be active
            new_modifier = bpy.context.object.modifiers.active

            # remove the newly create node group
            bpy.data.node_groups.remove(new_modifier.node_group)

            # assign the desired node group to this modifier
            new_modifier.node_group = bpy.data.node_groups[
                self.subpanel_gng_name
            ]

            # select that node group ---> self.subpanel_gng_name
            # select node under the cursor:  bpy.ops.node.select(
            # context.selected_nodes
            # context.active_node = bpy.data.node_groups[
            # self.subpanel_gng_name]

            # find location of node
            # only of node, rather than group? :?
            # bpy.data.node_groups['Geometry Nodes'].nodes['Group'].location

            # bpy.ops.node.select(
            #     deselect_all=True,
            #     select_passthrough=True,
            #     location=node_location
            # )

            # print(context.selected_nodes)

        # else: if its a 'simple' node group
        # toggle edit mode
        # bpy.ops.node.group_edit(exit=False)
        # print('No modifiers linked to this GNG')

        # # get the subpanel's material slot index
        # # returns -1 if there is no slot for that material
        # slot_idx_for_subpanel_gng = cob.material_slots.find(
        #     self.subpanel_material_name
        # )

        # # change active slot shown in graph
        # # NOTE: switching slot switches the active material too
        # if (
        #     slot_idx_for_subpanel_material == -1
        # ):  # if no slot for this material
        #     bpy.ops.object.material_slot_add()  # add a new slot
        #     cob.active_material_index = len(cob.material_slots) - 1
        # else:
        #     cob.active_material_index = slot_idx_for_subpanel_material

        # # check if the subpanel's material is the active one
        # # (when I switch slot the material switches too)
        # if (
        #     bpy.data.materials[self.subpanel_material_name]
        #     != cob.active_material
        # ):
        #     cob.active_material = bpy.data.materials[
        #         self.subpanel_material_name
        #     ]

        return {"FINISHED"}


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [RandomiseAllGeometryNodes]

for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    operator_i = type(
        f"ViewNodeGraphOneGNG_subpanel_{i}",
        (
            ViewNodeGraphOneGNG,
            bpy.types.Operator,
        ),
        {
            "bl_idname": f"node.view_graph_for_gng_{i}",
            "bl_label": "",
            "subpanel_gng_idx": i,
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
