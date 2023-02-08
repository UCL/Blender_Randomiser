"""
To run
    blender
    --python <path to this script>
    -- <space-separated list of paths to the addons to enable>
Example:
    blender
    --python ./blender_randomiser/install_and_enable_addons.py
    -- ./blender_randomiser/add_array_objects_to_cursor.py
    ./blender_randomiser/add_random_cube_in_volume.py


"""

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
    usage_text = (
        "To launch Blender and install+enable the desired add-ons, run:"
        "  blender --python "
        + __file__
        + " -- [list of paths to addons to install and enable]"
        "To launch Blender *with factory settings* add:"
        "  blender --factory-startup --python "
        + __file__
        + " -- [list of paths to addons to install and enable]"
    )
    parser = argparse.ArgumentParser(description=usage_text)

    # add arguments to parser
    # Possible types are: string, int, long, choice, float and complex.
    # required
    parser.add_argument(
        "addons_paths",
        nargs="*",
        type=str,
        metavar="ADDONS_PATHS",  # A name for the argument in usage messages.
        help="Space-separated list of the paths to the add-ons to enable",
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

    for p in args.addons_paths:
        ### Install the addons
        bpy.ops.preferences.addon_install(filepath=p)

        ### Enable them
        bpy.ops.preferences.addon_enable(module=Path(p).stem)

        # alternative using addon_utils:
        # https://blender.stackexchange.com/questions/32409/how-to-enable-and-disable-add-ons-via-python
        # addon_utils.enable(
        #     Path(p).stem,
        #     default_set=True, # if True, it will be synced with the userprefs
        #     # persistent=False # not sure what this does
        # (it is not presistency across sessions)
        # )

        ### Print
        print(f'"{Path(p).stem}" installed from source script and enabled')


if __name__ == "__main__":
    main()
