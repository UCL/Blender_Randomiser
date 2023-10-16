# Blender_Randomiser


Blender Randomiser is a Blender add-on that allows different Blender properties to be randomised between minimum and maximum bounds. This can be achieved either by:
 - Manually setting the bounds in the UI Randomiser panel located in the Geometry Nodes space
 - Using an input `.json` [file](/input_bounds.json) to set the bounds from the command line

## Purpose

The original and main use case of this add-on is for rendering synthetic (near) photo-realstic data for laparoscopic surgery, with a view to generating large scale labelled data sets for ML applications in surgery. With that context to replicate the different camera positions used in surgery as well as the shape and appearance of the tissues involved with surgery, the three main components (contained with separate UI panels) to be randomised are:
 - **Camera transforms** (location and Euler rotation)
 - **Geometry**
 - **Materials**

 Additionally, there is a **user defined properties** panel where the user can specify the full path of a property they want to randomised and it will create a subpanel for each of these properties with min-max bounds. Examples include:
  - bpy.context.scene.camera.location (Float 3D)
  - bpy.context.scene.frame_current (int 1D)
  - bpy.data.objects["Sphere"].scale (Float 3D)
  - bpy.data.objects["Cube"].collision.absorption (Float 1D)
  - bpy.data.cameras["Camera"].dof.aperture_fstop (Float 1D)
  - bpy.data.objects["Cube"].rotation_euler (Euler)

  Other functionality includes:
   - Seed panel to set the random seed
   - Randomise properties per frame
   - Save Parameter panel with outputs saved to `.json` [file](/output_randomisations_per_frame1697116725.310647.json) with a timestamp


 ## Installation
First, clone the repository in your desired directory
```
git clone https://github.com/UCL/Blender_Randomiser.git
```

## To install via command line
1. Launch a terminal at the cloned directory
    - You should be at the `Blender_Randomiser` directory
2. Run the following bash script:
    ```
    sh install_randomiser.sh
    ```
    - This will zip the `randomiser` subdirectory, open the `sample.blend` file with Blender, and use Blender's Python interpreter to execute the `install_and_enable_addons.py` script.
    - The `install_and_enable_addons.py` script installs and enables any add-ons that are passed as command line arguments (add-ons can be one Python file or a zip file)

Alternatively, install [manually](/doc/Install_addon_manually.md) via Blender settings

## To install via command line with additional inputs

For step 2 above, run the following bash script instead:

    sh install_randomiser.sh

This will follow the same steps as above, but there are optional inputs as well:
 - `--seed 32` which is an input to Blender
 - `--input ./input_bounds.json` (input to `install_and_enable_addons.py`)
 - `--output ./output_randomisations_per_frame1697116725.310647.json` (input to `install_and_enable_addons.py`)

## Learning and tutorials

[Add-on tutorial from docs](https://docs.blender.org/manual/en/3.4/advanced/scripting/addon_tutorial.html)

[Developer documentation: Python](https://wiki.blender.org/wiki/Python)


 ## License and copyright


 ## Testing

 [Testing script](/tests/test_integration/test_installing_and_enabling.py) which used [pytest-blender plugin](https://github.com/mondeja/pytest-blender#pytest-blender)

 To use the plugin, you need to install `pytest` and all other dependencies used in testing (`pytest-cov`) in the site-packages of Blender's Python. The repo provides some guidance for this [here](https://github.com/mondeja/pytest-blender#usage). It is important to make sure you use the correct Python interpreter and pip (Blender's ones) when installing `pytest` and `pytest-cov`.

 #### Linux:
 Running the following code in a script within Blender:

`import pip `

`pip.main(["install", "pytest", "--user"])`

`pip.main(["install", "pytest-cov", "--user"])`

`pip.main(["install", "pytest-blender", "--user"])`


 #### MacOS:

The following steps were need on MacOS:
 - `get-pip.py` downloaded (this step may not be needed since newer versions of Blender have pip installed already in the Blender python)
 - Changing Mac permissions to grant full disk access from where you're running pytest i.e. VS code or terminal
 - `/Applications/Blender.app/Contents/Resources/3.4/python/bin/python3.10 -m pip install pytest -t "/Applications/Blender.app/Contents/Resources/3.4/python/lib/python3.10/site-packages"` the target flag -t makes sure that the installation ends up in the correct place


 ### Running Tests

 Run `pytest` on the CLI within the project folder to test the camera transforms, materials and geometry panels as well as testing the `.blend` file loads, the add-on is installed and enabled and the randomising works per frame and with the seed set.

 N.B. Alternative approach would be to use [Blender as a python module](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule), but the only pytest-blender plugin approach is implemented in this repo.


 ## Dev notes

 Please see [Dev Notes](./doc/Dev_notes.md)


 ## Contributions
