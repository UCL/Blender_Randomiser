import random
from random import seed

import bpy
import numpy as np
from bpy.app.handlers import persistent
from mathutils import Euler, Vector

from .ui import attr_get_type, get_attr_only_str, get_obj_str


def attr_set_val(obj, path, min_val, max_val, UD_type):
    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
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

    # print("obj = ", path_attr)
    if UD_type == float:
        value = random.uniform(min_val, max_val)
        # print("1D float = ", value)
    elif UD_type == Vector:
        value = random.uniform(min_val, max_val)
        # print("3D Vector float = ", value)
    elif UD_type == Euler:
        deg2rad = np.pi / 180
        value = random.uniform(min_val, max_val)
        value = value * deg2rad
        # print("Euler = ", value)
    else:
        value = random.randint(min_val, max_val)
        # print("Integer = ", value)

    setattr(prop, path_attr, value)


class CUSTOM_OT_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Add and remove items"
    bl_options = {"REGISTER"}

    action_prop = bpy.props.EnumProperty(
        items=(
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
            if self.action == "REMOVE":
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({"INFO"}, info)

        if self.action == "ADD":
            item = scn.custom.add()
            item.name = "bpy.objects.data['Cube'].location"
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
# Operator Randomise selected
# User Defined Properties
# --------------------------------------------
class RandomiseAllUDProps(bpy.types.Operator):
    """Randomise the selected
    User Defined Properties

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
    bl_idname = "node.randomise_all_ud_sockets"  # this is appended to bpy.ops.
    bl_label = "Randomise selected sockets"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        """Determine whether the operator can be executed.

        The operator can only run if there are user defined properties
        in the collection. If it can't be executed, the
        button will appear as disabled.


        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            number of user defined properties in the collection
        """

        return len(context.scene.socket_props_per_UD.collection) > 0

    def invoke(self, context, event):
        """Initialise parmeters before executing the operator

        The invoke() function runs before executing the operator.
        Here, we
        - add the list of user defined properties and collection of
        user defined properties with associated info to the operator (self)

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
        # add list of UD props to operator self
        # NOTE: this list should have been updated already,
        # when drawing the panel

        cs = context.scene
        self.list_subpanel_UD_props_names = [
            UD.name for UD in cs.socket_props_per_UD.collection
        ]
        # for every UD prop: save name of UD prop
        self.sockets_to_randomise_per_UD = {}
        self.sockets_to_randomise_per_UD = []
        for UD_str in self.list_subpanel_UD_props_names:
            sckt = cs.socket_props_per_UD.collection[UD_str].name
            if cs.socket_props_per_UD.collection[UD_str].bool_randomise:
                self.sockets_to_randomise_per_UD.append(sckt)

        return self.execute(context)

    def execute(self, context):
        """Execute the randomiser operator

        Randomise the selected UD props between
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

        # For every UD prop with a subpanel
        for UD_str in self.sockets_to_randomise_per_UD:
            # get collection of socket properties for this UD prop
            # NOTE: socket properties do not include the actual socket object
            sockets_props_collection = cs.socket_props_per_UD.collection[
                UD_str
            ]

            full_str = sockets_props_collection.name
            attribute_only_str = get_attr_only_str(full_str)

            objects_in_scene = []
            for key in bpy.data.objects:
                objects_in_scene.append(key.name)

            if "[" in full_str:
                obj_str = get_obj_str(full_str)

                for i, obj in enumerate(objects_in_scene):
                    if obj in obj_str:
                        current_obj = obj
                        idx = i

                if "Camera" in current_obj:
                    attr_type = attr_get_type(
                        bpy.data.cameras[idx], attribute_only_str
                    )[0]
                else:
                    attr_type = attr_get_type(
                        bpy.data.objects[idx], attribute_only_str
                    )[0]

            elif "bpy.context.scene" in full_str:
                attr_type = attr_get_type(
                    bpy.context.scene, attribute_only_str
                )[0]

            # get min value for this UD prop
            min_val = np.array(
                getattr(
                    sockets_props_collection,
                    "min_" + cs.UD_prop_to_attr[attr_type],
                )
            )

            # get max value for this UD prop
            max_val = np.array(
                getattr(
                    sockets_props_collection,
                    "max_" + cs.UD_prop_to_attr[attr_type],
                )
            )

            if "[" in full_str:
                if "Camera" in full_str:
                    attr_set_val(
                        bpy.data.cameras[idx],
                        attribute_only_str,
                        min_val,
                        max_val,
                        attr_type,
                    )

                else:
                    attr_set_val(
                        bpy.data.objects[idx],
                        attribute_only_str,
                        min_val,
                        max_val,
                        attr_type,
                    )

            elif "bpy.context.scene" in full_str:
                attr_set_val(
                    bpy.context.scene,
                    attribute_only_str,
                    min_val,
                    max_val,
                    attr_type,
                )

        return {"FINISHED"}


# NOTE: without the persistent decorator,
# the function is removed from the handlers' list
# after it is first executed
@persistent
def randomise_UD_props_per_frame(dummy):
    bpy.ops.node.randomise_all_ud_sockets("INVOKE_DEFAULT")
    return


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

    bpy.app.handlers.frame_change_pre.append(randomise_UD_props_per_frame)

    print("UD operators registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(randomise_UD_props_per_frame)

    print("UD operators unregistered")
