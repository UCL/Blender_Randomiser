"""
To run in Blender from the terminal:
    blender
    --python <path to this script>
    -- <space-separated list of paths to the addons to enable>

Example:
    blender
    --python ./blender_randomiser/install_and_enable_addons.py
    -- ./blender_randomiser/add_array_objects_to_cursor.py
    ./blender_randomiser/add_random_cube_in_volume.py



"""

import json
from pathlib import Path
from random import seed

import bpy
import numpy as np


def main():
    import argparse
    import sys

    # get Python args (passed after "--")

    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1 :]  # get all args after "--"

    # ---------
    # initialise parser
    parser = argparse.ArgumentParser(
        description=(
            "To launch Blender and install+enable the desired add-ons, run:"
            "  blender --python "
            + __file__
            + " -- [list of paths to addons to install and enable OR"
            " path to parent dir]"
            ""
            "To launch Blender *with factory settings* add:"
            "  blender --factory-startup --python "
            + __file__
            + " -- [list of paths to addons to install and enable]"
        )
    )

    # add arguments
    # required (positonal)
    parser.add_argument(
        "addons_paths",
        nargs="*",
        type=str,  # types: string, int, long, choice, float and complex.
        metavar="ADDONS_PATHS",  # A name for the argument in usage messages.
        help="Space-separated list of the paths to the add-ons to enable OR"
        "path to parent dir",
    )

    parser.add_argument(
        "-s",
        "--seed",
        metavar="N",
        type=int,
        nargs="+",
        help="an integer for the randomisation seed",
    )

    parser.add_argument(
        "-i",
        "--input",
        nargs="*",
        type=str,  # types: string, int, long, choice, float and complex.
        metavar="INPUT_JSON_FILE",  # A name for argument in usage messages.
        help="Input .json file to set the min-max values for each panel",
    )

    # build parser object
    args = parser.parse_args(argv)

    # ---------
    # print help if no arguments provided
    if not argv:
        parser.print_help()
        return

    # error if required arguments not provided
    if not args.addons_paths:
        print("Error: paths to add-ons not provided, aborting.")
        parser.print_help()
        return
    # ---------

    # extract list of python files
    # TODO: option to exclude files (w regex?)
    if len(args.addons_paths) == 1 and Path(args.addons_paths[0]).is_dir():
        list_files = [
            str(item) for item in Path(args.addons_paths[0]).glob("*.py")
        ]

    else:  # TODO: check if list of paths?
        list_files = args.addons_paths

    # install and enable addons in list
    for p in list_files:
        bpy.ops.preferences.addon_install(filepath=p)
        bpy.ops.preferences.addon_enable(module=Path(p).stem)

        print(f'"{Path(p).stem}" installed from source script and enabled')

    if args.seed is not None:
        bpy.context.scene.seed_properties.seed = args.seed[0]
        seed(args.seed[0])
        bpy.context.scene.seed_properties.seed_toggle = True

    if args.input is not None:
        print("Yay!!!!!")
        print(args.input)
        path_to_file = args.input[0]
        with open(path_to_file, "r") as in_file_obj:
            text = in_file_obj.read()
            # convert the text into a dictionary
            data = json.loads(text)

        print(data["camera_pos_x_min"][0])

        loc_value_str = data["loc_value_str"]
        value_str = data["value_str"]
        if (
            loc_value_str == "delta_location"
            and value_str == "delta_rotation_euler"
        ):
            bpy.context.scene.randomise_camera_props.bool_delta = True
        else:
            loc_value_str = "location"
            value_str = "rotation_euler"
            bpy.context.scene.randomise_camera_props.bool_delta = False

        # bpy.data.objects['Camera'].location[0] = data["location"][0]
        getattr(bpy.context.scene.camera, loc_value_str)[0] = data["location"][
            0
        ]
        bpy.context.scene.randomise_camera_props.camera_pos_x_max[0] = data[
            "camera_pos_x_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_x_min[0] = data[
            "camera_pos_x_min"
        ][0]

        # bpy.data.objects['Camera'].location[1] = data["location"][1]
        getattr(bpy.context.scene.camera, loc_value_str)[1] = data["location"][
            1
        ]
        bpy.context.scene.randomise_camera_props.camera_pos_y_max[0] = data[
            "camera_pos_y_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_y_min[0] = data[
            "camera_pos_y_min"
        ][0]

        # bpy.data.objects['Camera'].location[2] = data["location"][2]
        getattr(bpy.context.scene.camera, loc_value_str)[2] = data["location"][
            2
        ]
        bpy.context.scene.randomise_camera_props.camera_pos_z_max[0] = data[
            "camera_pos_z_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_z_min[0] = data[
            "camera_pos_z_min"
        ][0]

        deg2rad = np.pi / 180

        rotation_mode = bpy.data.objects["Camera"].rotation_mode
        if rotation_mode in {"QUATERNION", "AXIS_ANGLE"}:
            bpy.data.objects["Camera"].rotation_mode = "XYZ"

        # bpy.data.objects['Camera'].rotation_euler[0]
        getattr(bpy.context.scene.camera, value_str)[0] = (
            data["rotation_euler"][0] * deg2rad
        )
        bpy.context.scene.randomise_camera_props.camera_rot_x_max[0] = data[
            "camera_rot_x_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_x_min[0] = data[
            "camera_rot_x_min"
        ][0]

        # bpy.data.objects['Camera'].rotation_euler[1]
        getattr(bpy.context.scene.camera, value_str)[1] = (
            data["rotation_euler"][1] * deg2rad
        )
        bpy.context.scene.randomise_camera_props.camera_rot_y_max[0] = data[
            "camera_rot_y_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_y_min[0] = data[
            "camera_rot_y_min"
        ][0]

        # bpy.data.objects['Camera'].rotation_euler[2]
        getattr(bpy.context.scene.camera, value_str)[2] = (
            data["rotation_euler"][2] * deg2rad
        )
        bpy.context.scene.randomise_camera_props.camera_rot_z_max[0] = data[
            "camera_rot_z_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_z_min[0] = data[
            "camera_rot_z_min"
        ][0]

        ## TO DO - invoke geometry and materials like in testing
        # to allow setting of min-max values
        # also dealing with multiple materials and sockets like in export
        # assign initial value
        # for m_str in ["min", "max"]:
        #     setattr(
        #         sckt_prop,
        #         m_str + "_" + socket_attrib_str,
        #         (ini_min_max_values[m_str],) * n_dim,
        #     )


if __name__ == "__main__":
    main()
