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
import re
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

    parser.add_argument(
        "-o",
        "--output",
        nargs="*",
        type=str,  # types: string, int, long, choice, float and complex.
        metavar="OUTPUT_JSON_FILE",
        # A name for argument in usage messages.
        help="Output .json save path and/or .json file for geom/mat names",
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

        if args.output is not None:
            out_path_to_file = args.output[0]
            with open(out_path_to_file, "r") as in_file_obj:
                text = in_file_obj.read()
                # convert the text into a dictionary
                out_data = json.loads(text)

            print(out_data["geometry"])

        else:
            print("no output file to pull names from")
        # set up some of the properties that will be needed for testing
        for obj in bpy.data.objects:
            if "Cube" in str(obj):
                pass
            elif "Sphere" in str(obj):
                pass
        # obj = bpy.data.objects[3] #Sphere
        bpy.context.view_layer.objects.active = obj
        bpy.context.scene.socket_props_per_gng.update_gngs_collection
        bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")

        # set range for randomise in blender properties
        sckts_list = []
        sckts_list.append("Values Geometry NodesRandomRadiusBottom")
        sckts_list.append("Values Geometry NodesRandomConeDepth")
        sckts_list.append("Values NodeGroupRandomRadiusBottom.001")
        sckts_list.append("Values NodeGroupRandomConeDepth.001")
        sckts_list.append("Values Geometry Nodes.001RandomSize")
        sckts_list.append("Values Geometry Nodes.001RandomSize.001")

        for current_sckt in sckts_list:
            print("input min-max from json ====== ", data[current_sckt])

        cs = bpy.context.scene
        for gng_idx in range(len(cs.socket_props_per_gng.collection)):
            # get this subpanel's GNG
            subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]
            print(subpanel_gng.name)

            cs.socket_props_per_gng.collection[
                subpanel_gng.name
            ].update_input_json

            # force an update in the sockets for this GNG
            cs.socket_props_per_gng.collection[
                subpanel_gng.name
            ].update_sockets_collection
            print("TEST Collection of Geometry Node Groups updated")

            sckt_prop = subpanel_gng.collection

            for sckt in subpanel_gng.collection:
                #        geom_current = {}
                print("sckt in sckt_prop = ", sckt)
                print(type(sckt))
                tmp_sck = sckt.name
                print(sckt.name)

                #        if "_Value" in tmp_sck:
                #            tmp_sck=tmp_sck.replace("_Value", "")
                #            print(tmp_sck)
                #        print(type(tmp_sck))

                #        sckt_cand = subpanel_gng.candidate_sockets
                #
                for s in subpanel_gng.candidate_sockets:
                    # build socket id from scratch
                    socket_id = s.node.name + "_" + s.name
                    print("socket_id ===== ")
                    print(socket_id)

                    if socket_id == tmp_sck:
                        sckt_val = s
                        break

                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt_val)
                ]

                # extract last number between '_' and 'd/D' in the
                # attribute name, to determine the shape of the array
                # TODO: there is probably a nicer way to do this...
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dictionary with initial min/max values
                # for this socket type
                #        ini_min_max_values = (
                #            bpy.context.scene.socket_type_to_ini_min_max[type(sckt_val)]
                #        )

                if "_Value" in tmp_sck:
                    tmp_sck = tmp_sck.replace("_Value", "")
                    print(tmp_sck)
                GNG_sck_values_str = subpanel_gng.name + tmp_sck
                GNG_sck_values_str = "Values " + GNG_sck_values_str
                print(GNG_sck_values_str)

                ini_min_max_values = data[GNG_sck_values_str]

                print(ini_min_max_values)
                print(sckt_prop)
                print(socket_attrib_str)
                print(n_dim)

                # assign initial value
                for m_str in ["min", "max"]:
                    setattr(
                        sckt,  # sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )


if __name__ == "__main__":
    main()
