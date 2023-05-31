import random

import bpy
import numpy as np
from bpy.app.handlers import persistent

from .. import config, utils


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
        # only node groups relevant to a specific object should
        # as enabled
        cs = context.scene
        cob = context.object

        # geometry node group of this subpanel
        subpanel_gng = cs.socket_props_per_gng.collection[cls.subpanel_gng_idx]

        # get list of node groups linked to modifiers of the active object
        list_gngs_in_modifiers = utils.get_gngs_linked_to_modifiers(cob)
        list_gngs_in_modifiers_names = [
            ng.name for ng in list_gngs_in_modifiers
        ]

        # get list of geometry node groups whose root parent
        # is a modfier-linked node group
        map_node_group_to_root_node_group = utils.get_map_inner_gngs(
            list_gngs_in_modifiers,
        )

        # get list of geometry node groups
        list_gngs = [
            gr.name for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
        ]

        # the GNG must be a Geometry node group, and either
        # - must be linked to a modifier of the currently active object
        # - must be a node group inside a node group linked to a modifier of
        # the currently active object (the inner node group can be
        # any levels deep)
        display_operator = (subpanel_gng.name in list_gngs) and (
            (subpanel_gng.name in list_gngs_in_modifiers_names)
            or (
                subpanel_gng.name
                in [gr.name for gr in map_node_group_to_root_node_group.keys()]
            )
        )

        return display_operator

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

        It shows the node graph for the geometry node group shown in the label.

        In practice, we change the graph view by changing the active modifier.
        Note as well that a modifier is defined for an object.

        It may be the case that a geometry node tree is not assigned
        to any modifier. In that case, if the view-graph button is clicked,
        a new modifier is added for that geometry node tree and for the
        currently active material.

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

        # find the modifier linked to this GNG, if exists
        subpanel_modifier = ""
        for mod in cob.modifiers:
            if (
                hasattr(mod, "node_group")
                and (hasattr(mod.node_group, "name"))
                and (self.subpanel_gng_name == mod.node_group.name)
            ):
                subpanel_modifier = mod
                break

        # get dict of inner geometry node groups
        list_gngs = [
            gr for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
        ]
        map_inner_node_groups_to_root_parent = utils.get_map_inner_gngs(
            list_gngs
        )

        # if there is a modifier linked to this GNG: set that
        # modifier as active (this will change the displayed graph)
        if subpanel_modifier:
            bpy.ops.object.modifier_set_active(modifier=subpanel_modifier.name)

            # ensure top level
            map_inner_gngs_of_modifier = utils.get_map_inner_gngs(
                [bpy.data.node_groups[self.subpanel_gng_name]]
            )
            max_depth = max(
                [v[1] for k, v in map_inner_gngs_of_modifier.items()]
            )
            # print(f'max depth for {self.subpanel_gng_name}: {max_depth}')
            for i in range(max_depth):  # max level
                bpy.ops.node.group_edit(exit=True)

            bpy.ops.node.select_all(action="DESELECT")

        # if there is no modifier linked to this GNG,
        # but the node group is an inner node group:
        # set root parent modifier as active and navigate to node
        elif not subpanel_modifier and (
            self.subpanel_gng_name
            in [gr.name for gr in map_inner_node_groups_to_root_parent.keys()]
        ):
            # find the modifier linked to the (root) parent and set as active
            # NOTE: if the parent is not linked to a modifier,
            # the operator is disabled
            root_parent_node_group = map_inner_node_groups_to_root_parent[
                bpy.data.node_groups[self.subpanel_gng_name]
            ][0]
            parent_modifier = ""
            for mod in cob.modifiers:
                if (
                    hasattr(mod, "node_group")
                    and (hasattr(mod.node_group, "name"))
                    and (root_parent_node_group.name == mod.node_group.name)
                ):
                    parent_modifier = mod
                    break
            bpy.ops.object.modifier_set_active(modifier=parent_modifier.name)
            # bpy.ops.node.select_all(action="DESELECT")

            # ensure we are at top level
            map_inner_gngs_of_modifier = utils.get_map_inner_gngs(
                [root_parent_node_group]
            )
            max_depth = max(
                [v[1] for k, v in map_inner_gngs_of_modifier.items()]
            )
            # print(max_depth)
            for i in range(max_depth):  # max level
                bpy.ops.node.group_edit(exit=True)  # go up

            ### compute list of parents nodes of this subpanel's GNG
            # in reverse order
            parent = utils.get_parent_of_gng(
                bpy.data.node_groups[self.subpanel_gng_name]
            )
            path_to_gng = [parent]
            while utils.get_parent_of_gng(parent) is not None:
                parent = utils.get_parent_of_gng(parent)
                path_to_gng.append(parent)

            path_to_gng.reverse()
            path_to_gng.append(bpy.data.node_groups[self.subpanel_gng_name])
            print(path_to_gng)

            # ### navigate to the selected node group
            for i, gng_step in enumerate(path_to_gng[1:]):
                # select parent node ---> do I need to set it as active?
                bpy.ops.node.select_all(action="DESELECT")

                selectable_gng = utils.get_selectable_node_for_node_group(
                    gng_step
                )
                selectable_gng.select = True
                # print(f'selectable: {selectable_gng}')

                # set parent node as active
                if path_to_gng[i] == root_parent_node_group:
                    root_parent_node_group.nodes.active = selectable_gng
                else:
                    selectable_parent_gng = (
                        utils.get_selectable_node_for_node_group(
                            path_to_gng[i]
                        )
                    )
                    selectable_parent_gng.node_tree.nodes.active = (
                        selectable_gng
                    )

                # print(f'active: {context.active_node}')

                # go one level down
                bpy.ops.node.group_edit(exit=False)

        # if there is no modifier linked to this GNG
        # and the node group is not an inner node group:
        # then create a new modifier and link the node group to it
        else:
            # Add a new 'Geometry nodes group' modifier
            # (will set it as active)
            bpy.ops.object.modifier_add(type="NODES")
            new_modifier = bpy.context.object.modifiers.active

            # assign the desired node group to this modifier
            new_modifier.node_group = bpy.data.node_groups[
                self.subpanel_gng_name
            ]

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
