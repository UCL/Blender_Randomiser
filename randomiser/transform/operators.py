from random import uniform

import bpy
import numpy as np
from bpy.app.handlers import persistent
from mathutils import Vector


# -------------------------------
## Operators
class ApplyRandomTransform(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise the position and orientation of the camera

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.apply_random_transform"  # appended to bpy.ops.
    bl_label = "Apply random transform to object"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        """Execute the randomiser operator

        Randomise the position and rotation x,y,z components
        of the camera between their min and max values.

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        loc = context.scene.randomise_camera_props.camera_pos
        rot = context.scene.randomise_camera_props.camera_rot

        loc_x_min = context.scene.randomise_camera_props.camera_pos_x_min[0]
        loc_x_max = context.scene.randomise_camera_props.camera_pos_x_max[0]
        loc_x_range = [loc_x_min, loc_x_max]

        loc_y_min = context.scene.randomise_camera_props.camera_pos_y_min[0]
        loc_y_max = context.scene.randomise_camera_props.camera_pos_y_max[0]
        loc_y_range = [loc_y_min, loc_y_max]

        loc_z_min = context.scene.randomise_camera_props.camera_pos_z_min[0]
        loc_z_max = context.scene.randomise_camera_props.camera_pos_z_max[0]
        loc_z_range = [loc_z_min, loc_z_max]

        rot_x_min = context.scene.randomise_camera_props.camera_rot_x_min[0]
        rot_x_max = context.scene.randomise_camera_props.camera_rot_x_max[0]
        rot_x_range = [rot_x_min, rot_x_max]

        rot_y_min = context.scene.randomise_camera_props.camera_rot_y_min[0]
        rot_y_max = context.scene.randomise_camera_props.camera_rot_y_max[0]
        rot_y_range = [rot_y_min, rot_y_max]

        rot_z_min = context.scene.randomise_camera_props.camera_rot_z_min[0]
        rot_z_max = context.scene.randomise_camera_props.camera_rot_z_max[0]
        rot_z_range = [rot_z_min, rot_z_max]
        delta_on = context.scene.randomise_camera_props.bool_delta

        # pdb.set_trace()

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
        )

        return {"FINISHED"}


@persistent
def randomise_camera_transform_per_frame(dummy):
    bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")

    return


# --------------------------------------------------
# Randomise_selected function:
def rand_num(min, max):
    return uniform(min, max)


def randomise_selected(
    context,  # seed, delta,
    loc,
    loc_x_range,
    loc_y_range,
    loc_z_range,
    rot,
    rot_x_range,
    rot_y_range,
    rot_z_range,
    delta_on,
):
    """Generate random numbers between the range for x/y/z
    directions in location and rotation

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # for obj in context.selected_objects:
    # pdb.set_trace()
    if loc:
        rand_x = rand_num(loc_x_range[0], loc_x_range[1])
        rand_y = rand_num(loc_y_range[0], loc_y_range[1])
        rand_z = rand_num(loc_z_range[0], loc_z_range[1])
        # pdb.set_trace()

        if delta_on:
            bpy.data.objects["Camera"].delta_location = Vector(
                [rand_x, rand_y, rand_z]
            )
        else:
            bpy.data.objects["Camera"].location = Vector(
                [rand_x, rand_y, rand_z]
            )

    else:  # otherwise the values change under us
        uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)

    if rot:
        rand_x = rand_num(rot_x_range[0], rot_x_range[1])
        rand_y = rand_num(rot_y_range[0], rot_y_range[1])
        rand_z = rand_num(rot_z_range[0], rot_z_range[1])
        vec = Vector([rand_x, rand_y, rand_z])
        deg2rad = np.pi / 180

        vec = vec * deg2rad  # convert degrees to radians

        rotation_mode = bpy.data.objects["Camera"].rotation_mode
        if rotation_mode in {"QUATERNION", "AXIS_ANGLE"}:
            bpy.data.objects["Camera"].rotation_mode = "XYZ"

        bpy.data.objects["Camera"].rotation_euler[0] = vec[0]  # in radians
        bpy.data.objects["Camera"].rotation_euler[1] = vec[1]
        bpy.data.objects["Camera"].rotation_euler[2] = vec[2]

        if delta_on:
            bpy.data.objects["Camera"].delta_rotation_euler[0] = vec[0]
            bpy.data.objects["Camera"].delta_rotation_euler[1] = vec[1]
            bpy.data.objects["Camera"].delta_rotation_euler[2] = vec[2]
        else:
            bpy.data.objects["Camera"].rotation_euler[0] = vec[0]
            bpy.data.objects["Camera"].rotation_euler[1] = vec[1]
            bpy.data.objects["Camera"].rotation_euler[2] = vec[2]
        bpy.data.objects["Camera"].rotation_mode = rotation_mode
    else:
        uniform(0.0, 0.0), uniform(0.0, 0.0), uniform(0.0, 0.0)


# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    ApplyRandomTransform,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(
        randomise_camera_transform_per_frame
    )

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(
        randomise_camera_transform_per_frame
    )

    print("unregistered")
