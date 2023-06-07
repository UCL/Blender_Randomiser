import json
import pathlib
from random import seed

import bpy
import numpy as np
from bpy.app.handlers import persistent

from ..transform.operators import get_transform_inputs, randomise_selected


# -------------------------------
# Operator
# -------------------------------
class ApplyRandomAll(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise all the panels

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.randomise_all"  # appended to bpy.ops.
    bl_label = "Apply randomisation to all panels"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the randomiser operator

        Randomise all the panels

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        (
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        ) = get_transform_inputs(context)

        randomise_selected(
            context,
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        )

        return {"FINISHED"}


# -------------------------------
class ApplySaveParams(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Save parameter outputs in .json

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.save_param_out"  # appended to bpy.ops.
    bl_label = "Save parameter outputs"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the save param operator

        Save parameter outputs in .json

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
            seed(bpy.data.scenes["Scene"].seed_properties.seed)

        bpy.data.scenes["Scene"].frame_current = 0
        tot_frame_no = bpy.context.scene.rand_all_properties.tot_frame_no
        x_pos_vals = []
        y_pos_vals = []
        z_pos_vals = []

        x_rot_vals = []
        y_rot_vals = []
        z_rot_vals = []

        if bpy.context.scene.randomise_camera_props.bool_delta:
            loc_value_str = "delta_location"
            value_str = "delta_rotation_euler"
        else:
            loc_value_str = "location"
            value_str = "rotation_euler"

        rad2deg = 180 / np.pi
        for idx in range(tot_frame_no):
            bpy.app.handlers.frame_change_pre[0]("dummy")
            bpy.data.scenes["Scene"].frame_current = idx

            x_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[0]
            )
            y_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[1]
            )
            z_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[2]
            )

            x_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[0] * rad2deg
            )
            y_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[1] * rad2deg
            )
            z_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[2] * rad2deg
            )

        data = {
            "location_str": loc_value_str,
            "loc_x": x_pos_vals,
            "loc_y": y_pos_vals,
            "loc_z": z_pos_vals,
            "rotation_str": value_str,
            "rot_x": x_rot_vals,
            "rot_y": y_rot_vals,
            "rot_z": z_rot_vals,
        }

        path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"

        with open(path_to_file, "w") as out_file_obj:
            # convert the dictionary into text
            text = json.dumps(data, indent=4)
            # write the text into the file
            out_file_obj.write(text)

        return {"FINISHED"}


@persistent
def randomise_all_per_frame(dummy):
    bpy.ops.camera.randomise_all("INVOKE_DEFAULT")

    return


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    ApplyRandomAll,
    ApplySaveParams,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(randomise_all_per_frame)

    print("randomise all operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(randomise_all_per_frame)

    print("randomise all unregistered")