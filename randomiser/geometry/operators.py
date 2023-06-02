import random

import bpy
import numpy as np
from bpy.app.handlers import persistent

from .. import config
from ..utils import node_groups as ng


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
        """Determine whether the operator can be executed.

        The operator can only run if there are geometry node groups
        in the collection. If it can't be executed, the
        button will appear as disabled.


        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            number of geometry node groups in the collection
        """

        return len(context.scene.socket_props_per_gng.collection) > 0

    def invoke(self, context, event):
        """Initialise parmeters before executing the operator

        The invoke() function runs before executing the operator.
        Here, we
        - add the list of input nodes and collection of socket properties to
          the operator (self), and
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
        # NOTE: this list should have been updated already,
        # when drawing the panel
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

        # For every GNG with a subpanel
        for gng_str in self.list_subpanel_gng_names:
            # get collection of socket properties for this material
            # NOTE: socket properties do not include the actual socket object
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

                # set default value
                # if socket type is boolean
                if type(sckt) == bpy.types.NodeSocketBool:
                    sckt.default_value = random.choice(
                        [bool(list(m_val)[0]) for m_val in [min_val, max_val]]
                    )  # 1d only
                    # TODO: change for a faster option?
                    # bool(random.getrandbits(1))F
                    # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python

                # if socket type is int
                elif type(sckt) == bpy.types.NodeSocketInt:
                    sckt.default_value = random.randint(max_val, min_val)

                # for all other socket types
                else:
                    # if type of the socket is NodeSocketColor,
                    # and max_val < min_val: switch them before randomising
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
                    sckt.default_value = random.uniform(min_val, max_val)

        return {"FINISHED"}


# NOTE: without the persistent decorator,
# the function is removed from the handlers' list
# after it is first executed
@persistent
def randomise_geometry_nodes_per_frame(dummy):
    bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")
    return


# -------------------------------
# Operator: view graph per GNG
# -------------------------------
class ViewNodeGraphOneGNG(bpy.types.Operator):
    """Show node graph for the relevant
    Geometry Node Group

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = (
        "gng.view_graph"  # this is appended to bpy.ops.
        # NOTE: it will be overwritten for each instance of
        # the operator
    )
    bl_label = "View node graph for this Geometry node group"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        """Determine whether the operator can be executed.

        This operator can only run if:
        - its geometry node group is of geometry type,
        and either:
        - the associated geometry node group is linked to a modifier
          of the currently active object, or
        - the associated geometry node group is an inner node and its
          root parent is a geometry node group linked to a modifier
          of the currently active object.

        An inner node is a geometry node group defined inside
        another geometry node group. The path of nodes to an inner
        node is the list of group nodes that leads to the inner node.
        Its root parent is the only parent node group in the path of nodes
        without a parent.

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

        cs = context.scene
        cob = context.object

        # get list of all GNGs
        list_gngs = [
            gr.name for gr in bpy.data.node_groups if gr.type == "GEOMETRY"
        ]

        # get geometry node group (GNG) of this subpanel
        subpanel_gng = cs.socket_props_per_gng.collection[cls.subpanel_gng_idx]

        # get list of GNGs linked to modifiers of the active object
        list_gngs_in_modifiers = ng.get_gngs_linked_to_modifiers(cob)
        list_gngs_in_modifiers_names = [
            ng.name for ng in list_gngs_in_modifiers
        ]

        # get list of (inner) GNGs whose root parent is a modfier-linked
        # GNG
        map_node_group_to_root_node_group = ng.get_map_inner_ngs_given_roots(
            list_gngs_in_modifiers,
        )

        # define condition to enable the operator
        display_operator = (
            subpanel_gng.name
            in list_gngs
            # TODO: maybe this is not required here?
        ) and (
            (subpanel_gng.name in list_gngs_in_modifiers_names)
            or (
                subpanel_gng.name
                in [gr.name for gr in map_node_group_to_root_node_group.keys()]
            )
        )

        return display_operator

    def invoke(self, context, event):
        """Initialise parmeters before executing the operator

        The invoke() function runs before executing the operator.
        Here, we add the subpanel's geometry node group name to
        the operator self

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

        cs = context.scene
        subpanel_gng = cs.socket_props_per_gng.collection[
            self.subpanel_gng_idx
        ]
        self.subpanel_gng_name = subpanel_gng.name

        return self.execute(context)

    def execute(self, context):
        """Execute the 'view graph' operator.

        It shows the graph for the geometry node group (GNG) shown in the
        subpanel's header.

        If the GNG associated to the subpanel is linked to a modifier of the
        active object, then that modifier is set to active and the graph
        is automatically updated.

        If the GNG  associated to the subpanel is NOT linked to a modifier, but
        it is an inner GNG of a modifier-linked GNG, then:
        - the modifier of the root parent GNG is set as active, and the graph
          is set to the root parent view
        - the path to the inner GNG is computed
        - the graph of the inner GNG is displayed, by recursively setting each
          parent node as active and then executing the 'edit node' command.


        If the GNG  associated to the subpanel is NOT linked to a modifier, and
        it is NOT an inner GNG of a modifier-linked GNG, then a new modifier
        will be added to the currently active material and this subpanel's GNG
        will be linked to it

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
        subpanel_modifier = ng.get_modifier_linked_to_gng(
            self.subpanel_gng_name, cob
        )

        # get dict of inner GNGs
        # the dict maps inner GNGs to a tuple made of its root parent GNG
        # and its depth
        map_inner_node_groups_to_root_parent = (
            ng.get_map_inner_ngs_given_roots(
                [gr for gr in bpy.data.node_groups if gr.type == "GEOMETRY"]
            )
        )

        # if there is a modifier linked to this GNG: set that
        # modifier as active (this will change the displayed graph)
        if subpanel_modifier:
            bpy.ops.object.modifier_set_active(modifier=subpanel_modifier.name)

            # ensure graph is at top level
            ng.set_ngs_graph_to_top_level(
                bpy.data.node_groups[self.subpanel_gng_name]
            )

        # if there is no modifier linked to this GNG,
        # but it is an inner GNG whose root parent is a modifier-linked GNG:
        # set the modifier as active and navigate the graph to the
        # inner GNG
        elif not subpanel_modifier and (
            self.subpanel_gng_name
            in [gr.name for gr in map_inner_node_groups_to_root_parent.keys()]
        ):
            # find the modifier linked to the (root) parent and set as active
            # NOTE: if the root parent is not linked to a modifier,
            # the operator will show as disabled
            root_parent_node_group = map_inner_node_groups_to_root_parent[
                bpy.data.node_groups[self.subpanel_gng_name]
            ][0]

            root_parent_modifier = ng.get_modifier_linked_to_gng(
                root_parent_node_group.name, cob
            )

            bpy.ops.object.modifier_set_active(
                modifier=root_parent_modifier.name
            )

            # compute the path to this subpanel's GNG
            # from the parent root GNG (both ends inclusive)
            path_to_gng = ng.get_path_to_ng(
                bpy.data.node_groups[self.subpanel_gng_name]
            )

            # ensure we are at the top level in the graph
            # (top level = parent root GNG)
            ng.set_ngs_graph_to_top_level(root_parent_node_group)

            # navigate the graph to the desired GNG
            # at every step: we set the target GNG as active and
            # click 'edit group'
            for i, _ in enumerate(path_to_gng[:-1]):
                # get target GNG for this step and its parent
                gng_parent = path_to_gng[i]
                gng_target = path_to_gng[i + 1]

                # get selectable version of the target GNG
                selectable_gng_target = ng.get_selectable_node_for_ng(
                    gng_target
                )

                # set target GNG as active
                if gng_parent == root_parent_node_group:
                    root_parent_node_group.nodes.active = selectable_gng_target
                else:
                    selectable_parent_gng = ng.get_selectable_node_for_ng(
                        gng_parent
                    )
                    selectable_parent_gng.node_tree.nodes.active = (
                        selectable_gng_target
                    )

                # click 'edit group', i.e. go one level down in the graph
                bpy.ops.node.group_edit(exit=False)

        # if there is no modifier linked to this GNG
        # and it is not an inner GNG: create a new modifier
        # for the currently active object and link the GNG to it
        else:
            # add a new 'Geometry nodes group' modifier
            # (will set it as active)
            bpy.ops.object.modifier_add(type="NODES")
            new_modifier = bpy.context.object.modifiers.active

            # assign the subpanel's GNGto this modifier
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
