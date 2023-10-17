# Blender_Randomiser


Blender Randomiser is a Blender add-on that allows different scene properties to be randomised between some minimum and maximum bounds. The bounds can be defined either by:
 - Manually setting the bounds in the UI Randomiser panel located in the Geometry Nodes space
 - Using an input `.json` [file](/input_bounds.json) to [set the bounds from the command line](/docs/input_output.md)

## Purpose

The add-on was originally developed to render a highly diverse and (near) photo-realistic synthetic dataset of laparoscopic surgery camera views. To replicate the different camera positions used in surgery as well as the shape and appearance of the tissues involved with surgery, we focused on three main components to randomise:
 - **Camera transforms** (location and Euler rotation with toggle for randomising in absolute or relative i.e. delta terms)
 - **Geometry** ([see further details](/docs/Materials_geometry_panel.md))
 - **Materials**([see further details](/docs/Materials_geometry_panel.md))

In the add-on, these three components appear as separate UI panels.

 Additionally, there is a **user-defined properties** panel where the user can specify the full Python path of a property to randomise.  When adding a user-defined property, a subpanel will be created to define its min and max bounds. Certain examples will and won't work (see [user-defined examples](/docs/user_defined_panel.md))

  Other functionality includes:
   - Selection toggle for including/excluding individual properties of the panel in the randomisation
   - Possibility of setting a randomisation seed for reproducibility
   - Capability to randomise the desired properties at every frame of an animation
   - [Save Parameter panel](/docs/input_output.md) with outputs saved to `.json` [file](/output_randomisations_per_frame1697116725.310647.json) with a timestamp


 ## Installation via command line
1. First, clone the repository in your desired directory
```
git clone https://github.com/UCL/Blender_Randomiser.git
```
2. Launch a terminal at the cloned directory
    - You should be at the `Blender_Randomiser` directory
3. Run the following bash script:
    ```
    sh install_randomiser.sh
    ```
    - This will zip the `randomiser` subdirectory, open the `sample.blend` file with Blender, and use Blender's Python interpreter to execute the `install_and_enable_addons.py` script.
    - The `install_and_enable_addons.py` script installs and enables any add-ons that are passed as command line arguments (add-ons can be passed as a path to a single Python file, or as a zip file)

> **Advanced Usage**
>  In step 3, run the [randomisation_seed.sh](/randomisation_seed.sh) bash script instead which has optional inputs:
> - `--seed 32` which is an input to Blender
> - `--input ./input_bounds.json` (input to `install_and_enable_addons.py`)
> - `--output ./output_randomisations_per_frame1697116725.310647.json` (input to `install_and_enable_addons.py`)

Alternatively, install [manually](/docs/Install_addon_manually.md) via Blender settings

 ## License and copyright

 [BSD 3-Clause License](/LICENSE)

 ## Testing

 1. Launch a terminal at the cloned directory
    - You should be at the `Blender_Randomiser` directory
 2. Run `pytest`
    - This will run our [testing script](/tests/test_integration/test_installing_and_enabling.py) which currently tests the camera transforms, materials and geometry panels.


> [!NOTE]
>  Only relevant if you are wanting to run the tests.
> The tests make use of the [pytest-blender plugin](https://github.com/mondeja/pytest-blender#pytest-blender), which has `pytest` and other packages as dependencies (e.g. `pytest-cov`). These need to be installed in the site-packages directory of Blender's Python. The pytest-blender repo provides some guidance for this [here](https://github.com/mondeja/pytest-blender#usage). It is important to make sure you use Blender's Python interpreter and Blender's pip when installing `pytest` and its dependencies. Below are some tips on how to do this in Linux and MacOS.

> **Linux**
>  An easy way to install these dependencies correctly in Linux is to run the following code in [Blender's Python scripting window](https://docs.blender.org/api/current/info_quickstart.html):
> `import pip `
`pip.main(["install", "pytest", "--user"])`
`pip.main(["install", "pytest-cov", "--user"])`
`pip.main(["install", "pytest-blender", "--user"])`


> **MacOS**
>  The following steps were needed to install these dependencies correctly on MacOS:
> - `get-pip.py` downloaded (this step may not be needed since newer versions of Blender have pip installed already in the Blender python)
> - Changing Mac permissions to grant full disk access from where you're running pytest i.e. VS code or terminal
> - `/Applications/Blender.app/Contents/Resources/3.4/python/bin/python3.10 -m pip install pytest -t "/Applications/Blender.app/Contents/Resources/3.4/python/lib/python3.10/site-packages"` the target flag -t makes sure that the installation ends up in the correct place

 ## Contributions

 Please see [Dev Notes](./docs/Dev_notes.md) if you wish to contribute. Feel free to submit suggestions via issues and/or PRs.
