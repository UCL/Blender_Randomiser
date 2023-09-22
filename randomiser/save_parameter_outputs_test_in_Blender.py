from random import seed

import bpy

if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
    seed(bpy.data.scenes["Scene"].seed_properties.seed)

bpy.data.scenes["Scene"].frame_current = 0
tot_frame_no = bpy.context.scene.rand_all_properties.tot_frame_no
x_pos_vals = []
y_pos_vals = []
z_pos_vals = []


x_rot_vals = []
y_rot_vals = []
z_rot_vals = []

if bpy.context.scene.randomise_camera_props.bool_delta:
    loc_value_str = "delta_location"
    value_str = "delta_rotation_euler"
else:
    loc_value_str = "location"
    value_str = "rotation_euler"


for idx in range(tot_frame_no):
    bpy.app.handlers.frame_change_pre[0]("dummy")
    bpy.data.scenes["Scene"].frame_current = idx

    x_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[0])
    y_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[1])
    z_pos_vals.append(getattr(bpy.context.scene.camera, loc_value_str)[2])

    x_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[0])
    y_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[1])
    z_rot_vals.append(getattr(bpy.context.scene.camera, value_str)[2])

data = {
    "location_str": loc_value_str,
    "loc_x": x_pos_vals,
    "loc_y": y_pos_vals,
    "loc_z": z_pos_vals,
    "rotation_str": value_str,
    "rot_x": x_rot_vals,
    "rot_y": y_rot_vals,
    "rot_z": z_rot_vals,
}
print(data)
# path_to_file = pathlib.Path.home() / "tmp" / "transform_test.json"
# print(path_to_file)

# with open(path_to_file, "w") as out_file_obj:
#     # convert the dictionary into text
#     text = json.dumps(data, indent=4)
#     # write the text into the file
#     out_file_obj.write(text)


# path_to_file = pathlib.Path.home() / "tmp" / "input_parameters.json"
#### TODO check file exists
# with open(path_to_file, "r") as in_file_obj:
#    text = in_file_obj.read()
#    # convert the text into a dictionary
#    data = json.loads(text)

## first_run = data["transform_x"]
