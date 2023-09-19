import json
import pathlib
from random import seed

import bpy

bpy.data.scenes["Scene"].seed_properties.seed_toggle = True
bpy.data.scenes["Scene"].seed_properties.seed = 3
seed(3)
bpy.data.scenes["Scene"].frame_current = 0
sequence_length = 5
first_run = []
for idx in range(sequence_length):
    bpy.app.handlers.frame_change_pre[0]("dummy")
    bpy.data.scenes["Scene"].frame_current = idx
    first_run.append(bpy.data.objects["Camera"].location[0])

data = {
    "transform_x": first_run,
}
print(data)
path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"
print(path_to_file)

with open(path_to_file, "w") as out_file_obj:
    # convert the dictionary into text
    text = json.dumps(data, indent=4)
    # write the text into the file
    out_file_obj.write(text)


path_to_file = pathlib.Path.home() / "tmp" / "input_parameters.json"
### TODO check file exists
with open(path_to_file, "r") as in_file_obj:
    text = in_file_obj.read()
    # convert the text into a dictionary
    data = json.loads(text)

## first_run = data["transform_x"]
