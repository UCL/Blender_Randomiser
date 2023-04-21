import bpy
import numpy as np

from . import config


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
    bl_idname = "node.randomise_all_sockets"  # this is appended to bpy.ops.
    bl_label = "Randomise selected sockets"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # operator can only run if there are materials in the collection
        return len(context.scene.socket_props_per_material.collection) > 0

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
        # add list of materials to operator self
        # (this list should have been updated already, when drawing the panel)
        cs = context.scene
        self.list_subpanel_material_names = [
            mat.name
            for mat in cs.socket_props_per_material.candidate_materials
        ]

        # for every material: save sockets to randomise
        self.sockets_to_randomise_per_material = {}
        for mat_str in self.list_subpanel_material_names:
            # get collection of socket properties for this material
            # ATT socket properties do not include the actual socket object
            sockets_props_collection = cs.socket_props_per_material.collection[
                mat_str
            ].collection

            # get candidate sockets for this material
            candidate_sockets = cs.socket_props_per_material.collection[
                mat_str
            ].candidate_sockets

            # if socket unlinked and randomisation toggle is True:
            # modify socket props to set toggle to False
            for sckt in candidate_sockets:
                # get socket identifier sting
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
                        f"Socket {sckt_id} from {mat_str} is unlinked:",
                        "randomisation toggle set to False",
                    )

            # after modifying randomisation toggle
            # - save list of sockets to randomise to dict
            # to dict, with key = material
            self.sockets_to_randomise_per_material[mat_str] = [
                sckt
                for sckt in candidate_sockets
                if sockets_props_collection[
                    sckt.node.name + "_" + sckt.name
                ].bool_randomise
            ]

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
        rng = np.random.default_rng()

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

                    # TODO: is there a more elegant way? feels a bit clunky....
                    max_val = max_val_new
                    min_val = min_val_new

                # assign randomised socket value
                sckt.default_value = rng.uniform(low=min_val, high=max_val)

        return {"FINISHED"}


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
        "node.view_graph"  # this is appended to bpy.ops. --will be overwritten
    )
    bl_label = "View node graph for this material"
    bl_options = {"REGISTER", "UNDO"}

    # link material to this operator ---added to each operator instance
    # subpanel_material_idx = 0

    @classmethod
    def poll(cls, context):
        # used to check if the operator can run.
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.candidate_materials[
            cls.subpanel_material_idx
        ]
        # TODO: have this here or in invoke?
        # cls.subpanel_material_name = subpanel_material.name
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
        # self is RandomiseMaterialNodes!!!
        cs = context.scene
        subpanel_material = cs.socket_props_per_material.candidate_materials[
            self.subpanel_material_idx
        ]
        self.subpanel_material_name = subpanel_material.name

        return self.execute(context)

    def execute(self, context):
        """Execute 'view graph' operator

        Show the node graph for this material

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
        cob.active_material = bpy.data.materials[self.subpanel_material_name]

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
            # why not directly material_str? --because here I cannot access
            # list of materials yet (restricted context)
        },
    )
    list_classes_to_register.append(operator_i)  # type: ignore


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("material operators registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("material operators unregistered")
