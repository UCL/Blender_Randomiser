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


def main():
    """
    User defined:
    --seed:     Randomisaiton Seed
    --input:    Input json file
    --output:   Output json file


    """
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

    # parser.add_argument(
    #    "-o",
    #    "--output",
    #    nargs="*",
    #    type=str,  # types: string, int, long, choice, float and complex.
    #    metavar="OUTPUT_JSON_FILE",
    #    # A name for argument in usage messages.
    #    help="Output .json save path and/or .json file for geom/mat names",
    # )

    # LB: Add frame number
    parser.add_argument(
        "-f",
        "--frame",
        nargs="*",
        type=int,  # types: string, int, long, choice, float and complex.
        # A name for argument in usage messages.
        help="Input frame number to render",
    )

    # LB: Add basename
    parser.add_argument(
        "-b",
        "--basename",
        nargs="*",
        type=str,  # types: string, int, long, choice, float and complex.
        # A name for argument in usage messages.
        help="Input basename number to render",
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
        Path(p).stem

        # LB if its already installed don't do anything
        # if addon_name not in bpy.context.preferences.addons:
        #    bpy.ops.preferences.addon_install(filepath=p)
        # if addon_name not in bpy.context.preferences.addons:
        #    bpy.ops.preferences.addon_enable(module=addon_name)
        print(p)

        bpy.ops.preferences.addon_install(filepath=p)
        print(Path(p).stem)
        bpy.ops.preferences.addon_enable(module=Path(p).stem)

        print(f'"{Path(p).stem}" installed from source script and enabled')

    if args.seed is not None:
        bpy.context.scene.seed_properties.seed = args.seed[0]
        seed(args.seed[0])
        bpy.context.scene.seed_properties.seed_toggle = True

    if args.input is not None:
        print("Input file for setting min-max boundaries")
        path_to_file = args.input[0]
        with open(path_to_file, "r") as in_file_obj:
            text = in_file_obj.read()
            # convert the text into a dictionary
            data = json.loads(text)

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

        bpy.context.scene.randomise_camera_props.camera_pos_x_max[0] = data[
            "camera_pos_x_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_x_min[0] = data[
            "camera_pos_x_min"
        ][0]

        bpy.context.scene.randomise_camera_props.camera_pos_y_max[0] = data[
            "camera_pos_y_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_y_min[0] = data[
            "camera_pos_y_min"
        ][0]

        bpy.context.scene.randomise_camera_props.camera_pos_z_max[0] = data[
            "camera_pos_z_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_pos_z_min[0] = data[
            "camera_pos_z_min"
        ][0]

        rotation_mode = bpy.data.objects["Camera"].rotation_mode
        if rotation_mode in {"QUATERNION", "AXIS_ANGLE"}:
            bpy.data.objects["Camera"].rotation_mode = "XYZ"

        bpy.context.scene.randomise_camera_props.camera_rot_x_max[0] = data[
            "camera_rot_x_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_x_min[0] = data[
            "camera_rot_x_min"
        ][0]

        bpy.context.scene.randomise_camera_props.camera_rot_y_max[0] = data[
            "camera_rot_y_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_y_min[0] = data[
            "camera_rot_y_min"
        ][0]

        bpy.context.scene.randomise_camera_props.camera_rot_z_max[0] = data[
            "camera_rot_z_max"
        ][0]
        bpy.context.scene.randomise_camera_props.camera_rot_z_min[0] = data[
            "camera_rot_z_min"
        ][0]

        ### GEOMETRY
        # if args.output is not None:
        #    out_path_to_file = args.output[0]
        #    with open(out_path_to_file, "r") as in_file_obj:
        #        text = in_file_obj.read()
        #        # convert the text into a dictionary
        #        out_data = json.loads(text)

        #    out_data["geometry"]
        #    print("Output file for key names provided")

        #    # Based on ouput file dictionary keys
        #    # TODO: - use output file keys and type of values
        #    # to replicated code below
        #
        # else:
        #    print(
        #        "No Output file for key names \
        #        provided - generate from .blend file objects"
        #    )

        # from testing function
        for obj in bpy.data.objects:
            if "Cube" in str(obj):
                active_obj = obj
            elif "Sphere" in str(obj):
                active_obj = obj
        # obj = bpy.data.objects[3] #Sphere

        bpy.context.view_layer.objects.active = active_obj
        bpy.context.scene.socket_props_per_gng.update_gngs_collection
        bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")

        # Based on random_all_save_params mainly
        cs = bpy.context.scene
        for gng_idx in range(len(cs.socket_props_per_gng.collection)):
            # get this subpanel's GNG
            subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]

            cs.socket_props_per_gng.collection[
                subpanel_gng.name
            ].update_input_json

            # force an update in the sockets for this GNG
            cs.socket_props_per_gng.collection[
                subpanel_gng.name
            ].update_sockets_collection
            print("INPUT Collection of Geometry Node Groups updated")

            for sckt in subpanel_gng.collection:
                tmp_sck = sckt.name

                for s in subpanel_gng.candidate_sockets:
                    # build socket id from scratch
                    socket_id = s.node.name + "_" + s.name

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
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                if "_Value" in tmp_sck:
                    tmp_sck = tmp_sck.replace("_Value", "")
                GNG_sck_values_str = subpanel_gng.name + tmp_sck
                GNG_sck_values_str = "Values " + GNG_sck_values_str

                ini_min_max_values = data[GNG_sck_values_str]

                # assign initial value
                for m_str in ["min", "max"]:
                    setattr(
                        sckt,  # sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )

        ### MATERIALS
        # if args.output is not None:
        #     out_path_to_file = args.output[0]
        #     with open(out_path_to_file, "r") as in_file_obj:
        #         text = in_file_obj.read()
        #         # convert the text into a dictionary
        #         out_data = json.loads(text)

        #     out_data["materials"]
        #     print("Output file for key names provided")

        #     # Based on ouput file dictionary keys
        #     # TODO: - use output file keys and type of values
        #     # to replicated code below

        # else:
        #     print(
        #         "No Output file for key names \
        #         provided - generate from .blend file objects"
        #     )

        bpy.context.scene.socket_props_per_material.update_materials_collection
        bpy.ops.node.randomise_all_material_sockets("INVOKE_DEFAULT")

        # Based on random_all_save_params and collection_socket_properties
        for mat_idx in range(len(cs.socket_props_per_material.collection)):
            # get this subpanel's GNG
            subpanel_material = cs.socket_props_per_material.collection[
                mat_idx
            ]

            cs.socket_props_per_material.collection[
                subpanel_material.name
            ].update_sockets_collection

            print("INPUT Collection of Materials updated")

            sockets_props_collection = subpanel_material.collection

            for sckt in sockets_props_collection:
                tmp_sck = sckt.name

                for s in subpanel_material.candidate_sockets:
                    # build socket id from scratch
                    socket_id = s.node.name + "_" + s.name

                    if s.node.id_data.name in bpy.data.node_groups:
                        socket_id = s.node.id_data.name + "_" + socket_id

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
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                if "_Value" in tmp_sck:
                    tmp_sck = tmp_sck.replace("_Value", "")

                mat_sck_values_str = subpanel_material.name + tmp_sck
                mat_sck_values_str = "Values " + mat_sck_values_str

                ini_min_max_values = data[mat_sck_values_str]

                # assign initial value
                for m_str in ["max", "min"]:
                    setattr(
                        sckt,  # sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )
        print("HERE")
        # RENDERING
        # Randomise geometry
        bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")

        # Set frame
        bpy.context.scene.frame_current = args.frame[0]
        # Set resolution and format
        bpy.context.scene.render.resolution_x = 554
        bpy.context.scene.render.resolution_y = 448
        bpy.context.scene.render.image_settings.file_format = "PNG"

        # Ensure render engine is set
        bpy.context.scene.render.engine = "CYCLES"  # or 'BLENDER_EEVEE'

        # Define and set the output path
        output_filename = (
            str(args.basename[0]) + "_f" + str(args.frame[0]) + ".png"
        )
        output_path = Path(output_filename)
        bpy.context.scene.render.filepath = str(output_path)

        # Render the image
        bpy.ops.render.render(write_still=True)

        # Set materials to segmentation
        red_material = bpy.data.materials.get("Red")
        black_material = bpy.data.materials.get("Black")

        # Get the node tree and the Set Material node
        node_tree = bpy.data.node_groups["Colon Geo Node"]
        set_material_node = node_tree.nodes["StalkPolypsMaterial"]
        set_material_node.inputs["Material"].default_value = red_material

        node_tree = bpy.data.node_groups["Colon Geo Node"]
        set_material_node = node_tree.nodes["SpherePolypsMaterial"]
        set_material_node.inputs["Material"].default_value = red_material

        node_tree = bpy.data.node_groups["Colon Geo Node"]
        set_material_node = node_tree.nodes["ColonMat1"]
        set_material_node.inputs["Material"].default_value = black_material

        node_tree = bpy.data.node_groups["Colon Geo Node"]
        set_material_node = node_tree.nodes["ColonMat2"]
        set_material_node.inputs["Material"].default_value = black_material

        node_tree = bpy.data.node_groups["Colon Geo Node"]
        set_material_node = node_tree.nodes["ColonMat3"]
        set_material_node.inputs["Material"].default_value = black_material

        # Render segmentation
        bpy.context.scene.frame_current = args.frame[0]
        # Set resolution and format
        bpy.context.scene.render.resolution_x = 554
        bpy.context.scene.render.resolution_y = 448
        bpy.context.scene.render.image_settings.file_format = "PNG"

        # Ensure render engine is set
        bpy.context.scene.render.engine = "CYCLES"  # or 'BLENDER_EEVEE'

        # Define and set the output path
        output_filename = (
            str(args.basename[0]) + "_seg" + str(args.frame[0]) + ".png"
        )
        output_path = Path(output_filename)
        bpy.context.scene.render.filepath = str(output_path)

        # Render the image
        bpy.ops.render.render(write_still=True)

        # print(set_material_node)
        # Set the material to "Red"
        # set_material_node.inputs[0].default_value = "Red"

        # ColonMat1
        # SpherePolypsMaterial

        # import math
        # from mathutils import Euler

        # angle_1 = math.radians(-166.92)
        # angle_2 = math.radians(-273.775)
        # angle_3 = math.radians(101.423)
        #
        # Apply to camera's rotation
        # camera = bpy.data.objects["Camera"]

        # print(camera.rotation_euler)
        # camera.rotation_euler = Euler((-2.91, -4.77, 1.77))
        # # Rotate 90 degrees around the X-axis
        # print(camera.rotation_euler)

        # print(bpy.data.node_groups["Colon Geo Node"].\
        # nodes["StalkPolypsMaterial"])

        # camera = bpy.data.objects["Camera"]
        # path = bpy.data.objects["BezierCurve"]

        # # Apply the Follow Path constraint to the camera
        # follow_path_constraint = camera.constraints.new(type="FOLLOW_PATH")
        # follow_path_constraint.target = path
        # follow_path_constraint.use_fixed_location = True
        # # Keeps the camera fixed along the path

        # # Ensure the camera is set to align forward along the curve
        # follow_path_constraint.forward_axis = 'FORWARD_Y'
        # # Aligns camera forward along the Y-axis

        # red_material = bpy.data.materials.get("Red")

        # # Get the node tree and the Set Material node
        # node_tree = bpy.data.node_groups["Colon Geo Node"]
        # set_material_node = node_tree.nodes["StalkPolypsMaterial"]
        # set_material_node.inputs["Material"].default_value = red_material

        # print(set_material_node)
        # # Set the material to "Red"
        # set_material_node.inputs[0].default_value = "Red"

        # Set frame
        # bpy.context.scene.frame_current = args.frame[0]

        # #camera = bpy.data.objects["Camera"]
        # #camera.rotation_euler = Euler((-2.9, -4.77, 1.77))
        # # Rotate 90 degrees around the X-axis

        # # Set frame
        # bpy.context.scene.frame_current = args.frame[0]
        # # Set resolution and format
        # bpy.context.scene.render.resolution_x = 554
        # bpy.context.scene.render.resolution_y = 448
        # bpy.context.scene.render.image_settings.file_format = 'PNG'

        # # Ensure render engine is set
        # bpy.context.scene.render.engine = 'CYCLES'
        # # or 'BLENDER_EEVEE'

        # # Define and set the output path
        # output_filename = str(args.basename[0]) + "_f" + \
        # str(args.frame[0]) + ".png"
        # output_path = Path(output_filename)
        # bpy.context.scene.render.filepath = str(output_path)

        # # Render the image
        # bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
