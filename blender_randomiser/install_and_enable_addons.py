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

import pdb
from pathlib import Path

import bpy


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
    pdb.set_trace()
    parser = argparse.ArgumentParser(
        description=(
            "To launch Blender and install+enable the desired add-ons, run:"
            "  blender --python "
            + __file__
            + " -- [list of paths to addons to install and enable OR"
            " path to parent dir]"
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
        "randomisation_seed",
        metavar="N",
        type=int,
        nargs="+",
        help="an integer for the accumulator",
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

    pdb.set_trace()
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

    pdb.set_trace()
    if (
        len(args.randomisation_seed) == 1
    ):  # ßßand args.randomisation_seed[0].is_int():
        pdb.set_trace()
        bpy.context.scene.randomise_camera_props.seed = (
            args.randomisation_seed[0]
        )

    pdb.set_trace()


if __name__ == "__main__":
    main()
