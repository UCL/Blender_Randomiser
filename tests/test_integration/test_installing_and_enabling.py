# This repo seems very useful for testing
# with pytest: https://github.com/mondeja/pytest-blender#pytest-blender
import subprocess
from pathlib import Path

import numpy as np
import pytest

try:
    import bpy
except ImportError:
    pytest.skip("bpy not available", allow_module_level=True)


# TODO:
# - make "randomiser" a fixture?
# - make sample.blend a fixture? keep it in test_data/?
def test_install_and_enable_1(
    blender_executable,  # pytest-blender fixture
    blender_addons_dir,  # pytest-blender fixture
):
    list_return_codes = []
    list_stderr = []

    # zip randomiser folder
    zip_result = subprocess.run(
        ["zip", "randomiser.zip", "-FS", "-r", "randomiser/"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    list_return_codes.append(zip_result.returncode)
    list_stderr.append(zip_result.stderr)

    # ----------------
    # Option 2:
    # launch blender with factory settings and sample blendfile
    blender_result = subprocess.run(
        [
            blender_executable,
            "--background",
            "--factory-startup",
            "sample.blend",
        ]
    )
    list_return_codes.append(blender_result.returncode)
    list_stderr.append(blender_result.stderr)

    # install and enable randomiser addon
    bpy.ops.preferences.addon_install(filepath="./randomiser.zip")
    bpy.ops.preferences.addon_enable(module=Path("randomiser.zip").stem)
    # ----------------

    # check addon is in expected folder
    directory_exists = Path.exists(Path(blender_addons_dir) / "randomiser")

    # TODO: maybe better practice to have all these in separate tests?
    assert (
        (all([x == 0 for x in list_return_codes]))
        and (all([x in ["", None] for x in list_stderr]))
        and (directory_exists)
    )


#####################
##   TRANSFORMS   ###
#####################


def test_randomiser_position():
    """Testing whether our randomizers generate poisitions
    within a specified range (between 1 and 3)."""

    # Define range of values we randomise over
    lower_bound = 1.0
    upper_bound = 3.0

    # set range for randomise in blender properties
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_x_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_x_min[
        0
    ] = lower_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_y_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_y_min[
        0
    ] = lower_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_z_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_pos_z_min[
        0
    ] = lower_bound

    # run a large number of randomisation and
    # check they fall with the predefined range
    total_random_test = 1000
    for _ in range(total_random_test):
        bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
        assert (
            (bpy.data.objects["Camera"].location[0] >= lower_bound)
            and (bpy.data.objects["Camera"].location[0] <= upper_bound)
            and (bpy.data.objects["Camera"].location[1] >= lower_bound)
            and (bpy.data.objects["Camera"].location[1] <= upper_bound)
            and (bpy.data.objects["Camera"].location[2] >= lower_bound)
            and (bpy.data.objects["Camera"].location[2] <= upper_bound)
        )


def test_randomiser_rotation():
    """Test our randomiser generates rotation angles
    between a specified range (between 10° and 90°)."""

    # Define range of values we randomise over
    lower_bound = 10.0
    upper_bound = 90.0

    # convert to radians
    deg2rad = np.pi / 180
    lower_bound_rad = lower_bound * deg2rad
    upper_bound_rad = upper_bound * deg2rad

    # set range for randomise in blender properties
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_x_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_x_min[
        0
    ] = lower_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_y_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_y_min[
        0
    ] = lower_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_z_max[
        0
    ] = upper_bound
    bpy.data.scenes["Scene"].randomise_camera_props.camera_rot_z_min[
        0
    ] = lower_bound

    # run a large number of randomisation
    # and check they fall with the predefined range
    total_random_test = 1000
    for _ in range(total_random_test):
        bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
        assert (
            (bpy.data.objects["Camera"].rotation_euler[0] >= lower_bound_rad)
            and (
                bpy.data.objects["Camera"].rotation_euler[0] <= upper_bound_rad
            )
            and (
                bpy.data.objects["Camera"].rotation_euler[1] >= lower_bound_rad
            )
            and (
                bpy.data.objects["Camera"].rotation_euler[1] <= upper_bound_rad
            )
            and (
                bpy.data.objects["Camera"].rotation_euler[2] >= lower_bound_rad
            )
            and (
                bpy.data.objects["Camera"].rotation_euler[2] <= upper_bound_rad
            )
        )


def test_random_seed():
    """Test whether changing the seed works by checking
    random numbers are the same after setting the same seed."""

    # Run randomisation 5 times and save some numbers
    bpy.data.scenes["Scene"].seed_properties.seed_toggle = True
    bpy.data.scenes["Scene"].seed_properties.seed = 1
    sequence_length = 5
    first_run = []
    for _ in range(sequence_length):
        bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
        first_run.append(bpy.data.objects["Camera"].location[0])

    # Change the sure and ensure the randomised numbers are different
    bpy.data.scenes["Scene"].seed_properties.seed = 2
    for idx in range(sequence_length):
        bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
        assert bpy.data.objects["Camera"].location[0] != first_run[idx]

    # Check that this randomisation outputs
    # the same numbers are the first for loop
    bpy.data.scenes["Scene"].seed_properties.seed = 1
    for idx in range(sequence_length):
        bpy.ops.camera.apply_random_transform("INVOKE_DEFAULT")
        assert bpy.data.objects["Camera"].location[0] == first_run[idx]


def test_bool_delta_position():
    pass


def test_bool_delta_rotation():
    pass


def test_per_frame():
    """Test if we can replicate a sequence of
    random numbers using the same seed when running an animation."""

    # Record the first few x positions
    # (randomly generated) in a sequence of frames
    bpy.data.scenes["Scene"].seed_properties.seed_toggle = True
    bpy.data.scenes["Scene"].seed_properties.seed = 3
    bpy.data.scenes["Scene"].frame_current = 0
    sequence_length = 5
    first_run = []
    for idx in range(sequence_length):
        bpy.app.handlers.frame_change_pre[0]("dummy")
        bpy.data.scenes["Scene"].frame_current = idx
        first_run.append(bpy.data.objects["Camera"].location[0])

    # Repeat the same sequence with a different seed,
    # then ensure the numbers generated are different
    bpy.data.scenes["Scene"].seed_properties.seed = 4
    bpy.data.scenes["Scene"].frame_current = 0
    for idx in range(sequence_length):
        bpy.app.handlers.frame_change_pre[0]("dummy")
        bpy.data.scenes["Scene"].frame_current = idx
        assert first_run[idx] != bpy.data.objects["Camera"].location[0]

    # Repeat sequence with original seed
    # and check if the numbers generated are the same
    bpy.data.scenes["Scene"].seed_properties.seed = 3
    bpy.data.scenes["Scene"].frame_current = 0
    for idx in range(sequence_length):
        bpy.app.handlers.frame_change_pre[0]("dummy")
        bpy.data.scenes["Scene"].frame_current = idx
        assert first_run[idx] == bpy.data.objects["Camera"].location[0]


def test_per_frame_bidirectional():
    """Test if frames in the animation sequence
    are the same going forward as going backwards."""

    # Run forward through a set of frames
    # in an animation and record the number generated
    bpy.data.scenes["Scene"].seed_properties.seed_toggle = True
    bpy.data.scenes["Scene"].seed_properties.seed = 5
    first_run = []
    for idx in range(7):
        bpy.data.scenes["Scene"].frame_current = idx
        bpy.app.handlers.frame_change_pre[0]("dummy")
        first_run.append(bpy.data.objects["Camera"].location[0])

    # Run backwards through the same frames as before,
    # ensuring that the numbers generated are the same
    for idx in range(4, -1, -1):
        bpy.data.scenes["Scene"].frame_current = idx
        bpy.app.handlers.frame_change_pre[0]("dummy")
        assert first_run[idx] == bpy.data.objects["Camera"].location[0]


# modified from the pytest-blender docs
def test_install_and_enable_2(install_addons_from_dir, uninstall_addons):
    # install and enable addons from directory
    addons_ids = install_addons_from_dir(
        ".", addons_ids=["randomiser"], save_userpref=False
    )

    # uninstall them
    uninstall_addons(addons_ids)
