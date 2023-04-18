# Blender_Randomiser

## Usage
First, clone the repository in your desired directory
```
git clone https://github.com/UCL/Blender_Randomiser.git
```

### To install via Blender settings
0. Zip the following directory:
    `Blender_Randomiser/blender_randomiser/randomiser/`
1. Launch Blender
2. Navigate to Edit > Preferences
3. On the left-hand side panel, select 'Add-ons'
4. On the top-right select 'Install an add-on'
3. Browse to select the randomiser.zip file.
    - In the background, Blender will copy the file to the add-ons folder and unzip it
    - In MacOS, this add-on directory is usually located at:
        `/Users/user/Library/Application Support/Blender/3.4/scripts/addons`
    (see [Blender directory layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html) for further details)

4. To enable the installed add-on, search for 'randomisation' in the top right search bar to find the add-on, and click on the checkbox to enable it.
    - Before searching, note that the checkbox to show enabled add-ons only ('Enabled Add-ons Only') may be selected!

Note that:
- if you install an add-on, it will overwrite any pre-existing add-ons with the same name.
- Blender will only have access to the add-ons copied to any of the add-ons directories (see [Blender directory layout](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html) for further details)
- remember that if you modify the code, you will need to create a new zip file with the latest version and repeat steps 1-4

## To install via command line
1. Launch a terminal at the cloned directory
    - You should be at the `Blender_Randomiser` directory
2. Run the following bash script:
    ```
    sh install_randomiser.sh
    ```
    - This will zip the `randomiser` subdirectory, open the `sample.blend` file with Blender, and use Blender's Python interpreter to execute the `install_and_enable_addons.py` script.
    - The `install_and_enable_addons.py` script installs and enables any add-ons that are passed as command line arguments (add-ons can be one Python file or a zip file)
