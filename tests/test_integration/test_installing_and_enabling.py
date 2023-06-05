# This repo seems very useful for testing
# with pytest: https://github.com/mondeja/pytest-blender#pytest-blender
import subprocess
from pathlib import Path

import bpy
import pytest


# add-on is uninstalled before each test (if it exists)
# all tests in this session can access the feature
# autouse: the fixture is automatically requested by all tests
@pytest.fixture(scope="session", autouse=True)
def uninstall_randomiser_addon(uninstall_addons):
    uninstall_addons(addons_ids=["randomiser"])


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

    # ----------
    # Option 1:
    # launch blender with factory settings and
    # run "install_and_enable_addons.py"
    # script
    # TODO: either test install_and_enable_addons.py separately or
    # do it here in simpler steps
    # blender_result = subprocess.run(
    #     [
    #         blender_executable,
    #         "--background",
    #         "--factory-startup",
    #         "sample.blend",
    #         "--python", "install_and_enable_addons.py",
    #         "--", "./randomiser.zip"
    #     ]
    # )

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


# modified from the pytest-blender docs
def test_install_and_enable_2(install_addons_from_dir, uninstall_addons):
    # install and enable addons from directory
    addons_ids = install_addons_from_dir(
        ".", addons_ids=["randomiser"], save_userpref=False
    )

    # uninstall them
    uninstall_addons(addons_ids)
