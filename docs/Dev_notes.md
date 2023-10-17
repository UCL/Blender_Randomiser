# Blender_Randomiser

Blender 3.4 uses Python 3.10.8.

This repository uses the cookiecutter template from the [SainsburyWellcomeCentre](https://github.com/SainsburyWellcomeCentre/python-cookiecutter)

## Python scripting in Blender
The docs provide a good list of first steps to get started with Python scripting, including enabling developer mode. See [here](https://docs.blender.org/api/current/info_quickstart.html).

Three main ways to run Python code in Blender:
- via the in-built TextEditor
- via the in-built Python console
- via the terminal

Useful resources:
- [Blender Python API docs](https://docs.blender.org/api/current/)
- [A guide to Scripting in Blender](https://docs.blender.org/manual/en/3.4/advanced/scripting/index.html) from the docs.
- [Using an external editor](https://docs.blender.org/api/current/info_tips_and_tricks.html#use-an-external-editor):
    ```python
        filename = "/full/path/to/myscript.py"
        exec(compile(open(filename).read(), filename, 'exec'))
    ```

> A handy (hidden) feature is that you can press Ctrl-C over any menu item or button to copy the command shown in the tooltip into the clipboard.


## Virtual environment for development
From [this discussion](https://blender.stackexchange.com/questions/181928/does-blender-use-a-python-virtual-environment):
- Blender has its own Python interpreter, modules and libraries and is therefore entirely separated from your system's Python installation(s).
- The interpreter is linked into Blender's binary.
- It does not create or use virtual environments.
- The add-ons and commands from the Python console are executed by the same Python interpreter and therefore have access to the same modules and libraries.


Things to be aware of re add-ons:

> There is no isolation or separate dependency management for each individual add-on. Hence, add-on developers need to be careful not to install packages that could conflict with other add-ons. Currently Blender has no unified way to install the required dependencies through the Python API. This also raises the question how the user is notified that the add-on requires additional packages. Depending on the location of Blender's directory, the installation may require elevated privileges


For development it is still advisable to work in a virtual environment, even if that is not the Python interpreter Blender will use... In this environment it is useful to install `fake-bpy-module` for autocomplete. I am using these requirements for the development virtual environment:
```
certifi==2022.12.7
fake-bpy-module-3.4==20230117
numpy==1.22.0
pip==22.3.1
setuptools==65.6.3
wheel==0.37.1
```

[Bundled Python and extensions](https://docs.blender.org/api/current/info_tips_and_tricks.html#bundled-python-extensions)


## Running Python script in Blender from the terminal

Running Blender from the terminal is useful for automation and batch processing which require launching Blender with different arguments.

When working from the terminal, it is convenient to [add Blender to the system path](https://docs.blender.org/manual/en/3.4/advanced/command_line/launch/index.html).

The full docs on running Blender from the terminal can be found [here](https://docs.blender.org/manual/en/3.4/advanced/command_line/index.html).


## Command line arguments for Blender
Below the main command line arguments for Blender are summarised. The full list can be found [here](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html).


- The following command will run the selected Python script in Blender and start the GUI. Typically the Python script will define a scene (geometry, virtual cameras, etc.) and its animation
    ```python
        path/to/blender/exe --python path/to/python/file.py
    ```

- To launch Blender 'headless', add the `--background` flag:
    ```python
        path/to/blender/exe --background --python path/to/python/file.py
    ```

- To pass command line arguments to the Python script, specify them after the empty flag `--` (`--` causes Blender to ignore all following arguments so Python can use them):
    ```python
        path/to/blender/exe --background --python path/to/python/file.py -- <command-line-args-for-python-script>
    ```

- To launch Blender 'headless' and render the animation defined in the script, add the `--render-anim` flag (short: `-a`). This will render all the frames in the animation from start to end:
    ```python
        path/to/blender/exe --background --python path/to/python/file.py --render-anim -- <command-line-args-for-python-script>
    ```
    It is also possible to render [a discont sequence of frames](https://docs.blender.org/manual/en/2.81/advanced/command_line/arguments.html)

- We may want to use `--factory-startup` to ignore any user defined settings when running Blender 'headless':
    ```python
        path/to/blender/exe --background --factory-startup --python path/to/python/file.py

    ```
- To run on an existing blend file:
    ```python
        blender myscene.blend --background --python myscript.py
    ```

- To run Blender from the terminal and enable an (already installed) add-on
    ```python
        blender --addons add_array_objects_to_cursor
    ```

## Scripting using Blender text editor
Running scripts from the text editor in Blender can be useful to explore / debug. The following template script is provided in Blender:
```python
# This stub runs a python script relative to the currently open
# blend file, useful when editing scripts externally.

import bpy
import os

# Use your own script name here:
filename = "my_script.py"

filepath = os.path.join(os.path.dirname(bpy.data.filepath), filename)
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)

```


## Add-ons


*An add-on is simply a Python module with some additional requirements so Blender can display it in a list with useful information.*


Addons are saved into one of (not sure why would it be one or the other)
```
    ['/Applications/Blender.app/Contents/Resources/3.4/scripts/addons',
    '/Users/user_account/Library/Application Support/Blender/3.4/scripts/addons',
    '/Applications/Blender.app/Contents/Resources/3.4/scripts/addons_contrib']
```

To install an add-on (maybe we have this command in the main.py file, called from the launching bash script?):
```python
    bpy.ops.preferences.addon_install()
```


To enable an already installed add-on from the CLI:
```python
    blender --addons add_array_objects_to_cursor
```

[Accepted space-regions combinations](https://blender.stackexchange.com/a/97268)


---

## Other notes on Python scripting in Blender

From experience the easiest way to work with Blender add-ons is by loading scripts containing snippets of code you want to test in [Blender's Python scripting window](https://docs.blender.org/api/current/info_quickstart.html) at the same time as your add-on/panel to allow interaction of your code with your add-on and to allow access to the Blender scene properties. Alternatively, there are other options to debug and inspect variables (see below).

### To inspect variables / debug:

- #### Option 1:  Use 'code' module
    Works in Python interactive terminal in Blender and in Windows terminal). See further info in [docs](https://docs.blender.org/api/2.81/info_tips_and_tricks.html#drop-into-a-python-interpreter-in-your-script). For me, pdb works if run from terminal but not with Python console in Blender
    ```
    import code
    code.interact(local=locals()) # place at the point you'd like to inspect
    ```
- #### Option 2: use IPython
    ```
    import IPython
    IPython.embed()
    ```

- #### Option 3: use pdb
    run from Blender gui after opening Python terminal from Blender (a bit buggy tho, sometimes Blender crashes)

### To get path to Python executable:
    bpy.app.binary_path_pythonbp

### Useful resources
- http://web.purplefrog.com/~thoth/blender/python-cookbook/
- https://docs.blender.org/api/current/info_tips_and_tricks.html
- https://docs.blender.org/manual/en/2.81/advanced/command_line/arguments.html
- Python templates in the TextEditor panel in Blender
