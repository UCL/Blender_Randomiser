import random
from random import seed

import bpy
import numpy as np
from mathutils import Vector

from .ui import attr_get_type, get_attr_only_str, get_obj_str


def attr_set_val(obj, path, min_val, max_val, UD_type):
    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
        # len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS))
        path_prop, path_attr = path.rsplit(".", 1)

        # same as: prop = obj.modifiers["Subsurf"]
        prop = obj.path_resolve(path_prop)
    else:
        prop = obj
        # single attribute such as name, location... etc
        path_attr = path

    # same as: prop.levels = value

    try:
        getattr(prop, path_attr)
    except Exception:
        # print("Property does not exist")
        pass
    # action = getattr(prop, path_attr)

    print("attr_set_val type ========================= ", UD_type)

    if UD_type == float:
        print("HELLO 1D FLOAT!!!!!!!")
        value = random.uniform(min_val, max_val)
        print(value)
    elif UD_type == Vector:
        print("HELLO 3D VECTOR FLOAT!!!!!")
        value = random.uniform(min_val, max_val)
        print(value)
    else:
        print("HELLO INTEGER!!!!!!!!!!!!!!!!!!!!")
        value = random.randint(min_val, max_val)
        print(value)

    setattr(prop, path_attr, value)


class CUSTOM_OT_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {"REGISTER"}

    action_prop = bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("REMOVE", "Remove", ""),
            ("ADD", "Add", ""),
        )
    )
    action: action_prop  # type: ignore

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == "DOWN" and idx < len(scn.custom) - 1:
                scn.custom[idx + 1].name
                scn.custom.move(idx, idx + 1)
                scn.custom += 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    scn.custom + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "UP" and idx >= 1:
                scn.custom[idx - 1].name
                scn.custom.move(idx, idx - 1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    scn.custom_index + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "REMOVE":
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({"INFO"}, info)

        if self.action == "ADD":
            item = scn.custom.add()
            item.name = "bpy.context.scene.camera.ranch"
            item.id = len(scn.custom)
            scn.custom_index = len(scn.custom) - 1
            info = '"%s" added to list' % (item.name)
            self.report({"INFO"}, info)
        return {"FINISHED"}


class CUSTOM_OT_printItems(bpy.types.Operator):
    """Print all items and their properties to the console"""

    bl_idname = "custom.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {"REGISTER", "UNDO"}

    reverse_order_prop = bpy.props.BoolProperty(
        default=False, name="Reverse Order"
    )
    reverse_order: reverse_order_prop  # type: ignore

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.custom, -1, -1):
                item = scn.custom[i]
                print("Name:", item.name, "-", "ID:", item.id)
        else:
            for item in scn.custom:
                print("Name:", item.name, "-", "ID", item.id)
        return {"FINISHED"}


class CUSTOM_OT_clearList(bpy.types.Operator):
    """Clear all items of the list"""

    bl_idname = "custom.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({"INFO"}, "All items removed")
        else:
            self.report({"INFO"}, "Nothing to remove")
        return {"FINISHED"}


# --------------------------------------------
# Operator Randomise selected sockets
# across all Geometry node groups
# --------------------------------------------
##### REFACTOR - remove to replace with randomise all?
class RandomiseAllUDProps(bpy.types.Operator):
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
    bl_idname = "opr.randomise_all_ud_sockets"  # this is appended to bpy.ops.
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

        return len(context.scene.socket_props_per_UD.collection) > 0

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

        print("INVOKE!!!! ")
        cs = context.scene
        self.list_subpanel_UD_props_names = [
            UD.name for UD in cs.socket_props_per_UD.collection
        ]
        # for every GNG: save sockets to randomise
        self.sockets_to_randomise_per_UD = {}
        self.sockets_to_randomise_per_UD = []
        for UD_str in self.list_subpanel_UD_props_names:
            # if cs.socket_props_per_UD.collection[
            #     UD_str
            # ].update_UD_props_collection:
            #     print("Collection of UD props updated")

            # sockets_props_collection = cs.socket_props_per_gng.collection[
            #     gng_str
            # ].collection

            # get candidate sockets for this GNG
            # candidate_sockets = cs.socket_props_per_UD.collection[
            #     UD_str
            # ].candidate_sockets

            #### REFACTOR to invalid prop instead of unlinked geom sckt
            #### OPTION 1 for loop witin for loop cand_sockets
            # if socket unlinked and randomisation toggle is True:
            # modify socket props to set toggle to False
            # self.socket_props_per_UD[UD_str] = []
            # for sckt in candidate_sockets:
            #     print('sck for loop ===== ', sckt)
            #     if cs.socket_props_per_UD.collection[UD_str].bool_randomise:
            #         self.sockets_to_randomise_per_UD[UD_str].append(sckt)

            #### REFACTOR to invalid prop instead of unlinked geom sckt
            #### OPTION 2 skip for loop for cand_sockets
            # if this UD is selected to randomise but it is invalid property:
            # set randomisation toggle to False
            # if (not sckt.is_linked) and (
            #     sockets_props_collection[sckt_id].bool_randomise
            # ):
            #     setattr(
            #         sockets_props_collection[sckt_id],
            #         "bool_randomise",
            #         False,
            #     )
            #     print(
            #         f"Socket {sckt_id} from {gng_str} is unlinked:",
            #         "randomisation toggle set to False",
            #     )

            sckt = cs.socket_props_per_UD.collection[UD_str].name
            if cs.socket_props_per_UD.collection[UD_str].bool_randomise:
                self.sockets_to_randomise_per_UD.append(sckt)

            print(
                "INVOKE ==== sockets to randomise ",
                list(self.sockets_to_randomise_per_UD),
            )

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

        previous_seed = cs.seed_properties.seed_previous
        current_seed = cs.seed_properties.seed
        seed_enabled = cs.seed_properties.seed_toggle
        if (previous_seed != current_seed) and (seed_enabled is True):
            seed(current_seed)
            cs.seed_properties.seed_previous = current_seed

        # For every GNG with a subpanel - REFACTORING BASED ON NEW CODE
        print(
            "EXECUTE list_subpanel_prop_names ==== ",
            self.sockets_to_randomise_per_UD,
        )
        # for UD_str in self.list_subpanel_UD_props_names:
        for UD_str in self.sockets_to_randomise_per_UD:
            # get collection of socket properties for this material
            # NOTE: socket properties do not include the actual socket object
            sockets_props_collection = cs.socket_props_per_UD.collection[
                UD_str
            ]

            # #### Modify to set_attr !!!!!!!
            full_str = sockets_props_collection.name
            attribute_only_str = get_attr_only_str(full_str)

            print("ATTRIBUTE ONLY STRING ======== ", attribute_only_str)

            objects_in_scene = []
            for key in bpy.data.objects:
                objects_in_scene.append(key.name)

            if "[" in full_str:
                print("bpy.context.scene")
                print("OPS EXECUTE attribute_only_str ", attribute_only_str)
                obj_str = get_obj_str(full_str)
                # print(obj_str)

                for i, obj in enumerate(objects_in_scene):
                    #        regex=re.compile(r'^test-\d+$')

                    if obj in obj_str:
                        print("Yay found cube")

                        idx = i

                attr_type = attr_get_type(
                    bpy.data.objects[idx], attribute_only_str
                )[0]
            elif "bpy.context.scene" in full_str:
                attr_type = attr_get_type(
                    bpy.context.scene, attribute_only_str
                )[0]

            # get min value for this socket
            min_val = np.array(
                getattr(
                    sockets_props_collection,
                    "min_" + cs.UD_prop_to_attr[attr_type],
                )
            )

            # get max value for this socket
            max_val = np.array(
                getattr(
                    sockets_props_collection,
                    "max_" + cs.UD_prop_to_attr[attr_type],
                )
            )

            if "[" in full_str:
                print("bpy.context.scene")
                print("OPS EXECUTE attribute_only_str ", attribute_only_str)

                attr_set_val(
                    bpy.data.objects[idx],
                    attribute_only_str,
                    min_val,
                    max_val,
                    attr_type,
                )

            elif "bpy.context.scene" in full_str:
                print("bpy.context.scene")
                print("OPS EXECUTE attribute_only_str ", attribute_only_str)
                attr_set_val(
                    bpy.context.scene,
                    attribute_only_str,
                    min_val,
                    max_val,
                    attr_type,
                )

        # # get min value for this socket
        #     min_val = np.array(
        #         getattr(
        #             sockets_props_collection[socket_id],
        #             "min_" + cs.socket_type_to_attr[type(sckt)],
        #         )
        #     )

        #     # get max value for this socket
        #     max_val = np.array(
        #         getattr(
        #             sockets_props_collection[socket_id],
        #             "max_" + cs.socket_type_to_attr[type(sckt)],
        #         )
        #     )

        #     # set default value
        #     # if socket type is boolean
        #     #### WHERE IS DEFAULT VALUE - ADD TO UI.PY TO APPEAR ON PANEL
        #     if type(sckt) == bpy.types.BoolProperty:
        #         sckt.default_value = random.choice(
        #             [bool(list(m_val)[0]) for m_val in [min_val, max_val]]
        #         )  # 1d only
        #         # TODO: change for a faster option?
        #         # bool(random.getrandbits(1))F
        #         # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python

        #     # if socket type is int
        #     elif type(sckt) == bpy.types.IntProperty:
        #         sckt.default_value = random.randint(max_val, min_val)

        #     # for all other socket types
        #     else:
        #         # if type of the socket is NodeSocketColor,
        #         # and max_val < min_val: switch them before randomising
        #         # NOTE: these are not switched in the display panel
        #         # (this is intended)
        #         if (type(sckt) == bpy.types.NodeSocketColor) and any(
        #             max_val < min_val
        #         ):
        #             max_val_new = np.where(
        #                 max_val >= min_val, max_val, min_val
        #             )
        #             min_val_new = np.where(
        #                 min_val < max_val, min_val, max_val
        #             )

        #             # TODO: is there a more elegant way?
        #             # feels a bit clunky....
        #             max_val = max_val_new
        #             min_val = min_val_new

        #         # assign randomised socket value
        #         sckt.default_value = random.uniform(min_val, max_val)

        return {"FINISHED"}

        # # sckt = list_UD_props_sorted  # UD.name
        # sckt = sockets_props_collection.name
        # # Loop through the sockets to randomise
        # for sckt in self.sockets_to_randomise_per_UD[UD_str]:
        #     socket_id = "sckt.node.name" + "_" + sckt.name

        #         # get min value for this socket
        #         min_val = np.array(
        #             getattr(
        #                 sockets_props_collection[socket_id],
        #                 "min_" + cs.socket_type_to_attr[type(sckt)],
        #             )
        #         )

        #         # get max value for this socket
        #         max_val = np.array(
        #             getattr(
        #                 sockets_props_collection[socket_id],
        #                 "max_" + cs.socket_type_to_attr[type(sckt)],
        #             )
        #         )

        #         # set default value
        #         # if socket type is boolean
        #         if type(sckt) == bpy.types.BoolProperty:
        #             sckt.default_value = random.choice(
        #                 [bool(list(m_val)[0]) for m_val in
        # [min_val, max_val]]
        #             )  # 1d only
        #             # TODO: change for a faster option?
        #             # bool(random.getrandbits(1))F
        #             # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python

        #         # if socket type is int
        #         elif type(sckt) == bpy.types.IntProperty:
        #             sckt.default_value = random.randint(max_val, min_val)

        #         # for all other socket types
        #         else:
        #             # if type of the socket is NodeSocketColor,
        #             # and max_val < min_val: switch them before randomising
        #             # NOTE: these are not switched in the display panel
        #             # (this is intended)
        #             if (type(sckt) == bpy.types.NodeSocketColor) and any(
        #                 max_val < min_val
        #             ):
        #                 max_val_new = np.where(
        #                     max_val >= min_val, max_val, min_val
        #                 )
        #                 min_val_new = np.where(
        #                     min_val < max_val, min_val, max_val
        #                 )

        #                 # TODO: is there a more elegant way?
        #                 # feels a bit clunky....
        #                 max_val = max_val_new
        #                 min_val = min_val_new

        #             # assign randomised socket value
        #             sckt.default_value = random.uniform(min_val, max_val)

        # return {"FINISHED"}


# NOTE: without the persistent decorator,
# the function is removed from the handlers' list
# after it is first executed
# @persistent
# def randomise_geometry_nodes_per_frame(dummy):
#     bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")
#     return


# Graph function removed - not needed?


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    RandomiseAllUDProps,
    CUSTOM_OT_actions,
    CUSTOM_OT_printItems,
    CUSTOM_OT_clearList,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    # bpy.app.handlers.frame_change_pre.append(
    #     randomise_geometry_nodes_per_frame
    # )

    print("UD operators registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # bpy.app.handlers.frame_change_pre.remove(
    #     randomise_geometry_nodes_per_frame
    # )

    print("UD operators unregistered")
