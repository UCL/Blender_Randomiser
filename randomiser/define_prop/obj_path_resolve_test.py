import random
import re

import bpy
import numpy as np
from mathutils import Vector


# %%
def get_obj_str(full_str):
    full_str = "bpy.data.objects['Cube'].location"
    # path_prop, path_attr = full_str.rsplit("[]", 1)
    x = full_str.split(".")
    # print(path_prop)
    for i in x:
        print(i)
        if "[" in i:
            ii = i.split("[")
            fiinal = ii[1]
            fiinal = fiinal[:-1]
            print("fiinal= ", fiinal)

    print(type(fiinal))
    print(fiinal)
    return fiinal


# %%


def attr_get_type(obj, path):
    # if '[' in path:
    #     print(' [ is in path')

    a = re.findall("\[(.*?)\]", path)
    if a:
        nums = list(map(int, a[0].split(",")))
        print(nums)
        print(type(str(nums[0])))
    else:
        nums = []

    print("len", len(nums))

    if len(nums) > 0:
        print("Number is ", nums)
        print("type(Number) is ", type(nums[0]))

        num_str = str(nums[0])

        tmp_UD_name = path
        tmp_UD_name = tmp_UD_name.replace("[" + num_str + "]", "")
        new_attribute_only_str = path.replace("[" + num_str + "]", "")

        print("new_attribute_only_str", new_attribute_only_str)
        path = new_attribute_only_str

        if "." in path:
            # gives us: ('modifiers["Subsurf"]', 'levels')
            path_prop, path_attr = path.rsplit(".", 1)

            # same as: prop = obj.modifiers["Subsurf"]
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            # single attribute such as name, location... etc
            path_attr = path

    else:
        if "." in path:
            # gives us: ('modifiers["Subsurf"]', 'levels')
            path_prop, path_attr = path.rsplit(".", 1)

            # same as: prop = obj.modifiers["Subsurf"]
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            # single attribute such as name, location... etc
            path_attr = path

    # same as: prop.levels = value

    print("prop = ", prop)
    print("path_attr = ", path_attr)

    try:
        #        action = getattr(prop, path_attr)
        #        print('action = ', action)
        #        print('type(action) = ', type(action))
        if len(nums) > 0:
            action = getattr(prop, path_attr)
            print("action = ", action)
            action = action[0]
            print("action = ", action)
            print("type(action) = ", type(action))
        else:
            action = getattr(prop, path_attr)
            print("action = ", action)
            print("type(action) = ", type(action))
    except Exception:
        # print("Property does not exist")
        action = "dummy"
        prop = "dummy"
        path_attr = "dummy"
        # print(action, prop, path_attr)
        # print(type(action))
    # action = getattr(prop, path_attr)

    return type(action), action, prop, path_attr
    # setattr(prop, path_attr, value)


# print("CAMERA.LOCATION !!!!!!!!!!!!!!!")
# print("INPUTS ======")
# attr_str = "camera.location"
# print("bpy.context.scene as obj and str = ", attr_str)
# action_type, action, prop, path_attr = attr_get_type(
#    bpy.context.scene, attr_str
# )
# print("OUTPUTS ===== ")
# print("type(action) = ", action_type)
# print("action = ", action)
# print("prop = ", prop)
# print("path_attr = ", path_attr)

##print("FRAME_CURRENT !!!!!!!!!!!!!!!")
##print("INPUTS ======")
##attr_str = "frame_current"
##print("bpy.context.scene as obj and str = ", attr_str)
##action_type, action, prop, path_attr = attr_get_type(
##    bpy.context.scene, attr_str
##)
##print("OUTPUTS ===== ")
##print("type(action) = ", action_type)
##print("action = ", action)
##print("prop = ", prop)
##print("path_attr = ", path_attr)


## bpy.context.scene.objects['Cube'].collision.absorption
## bpy.data.objects['Cube'].location
## bpy.data.objects['Cube'].rotation_euler.x
# print("bpy.data.objects[Cube] + string !!!!!!!!!!!!!!!")
# print("INPUTS ======")
##attr_str = 'location'
# attr_str = 'rotation_euler.x'
##attr_str = "collision.absorption"
# print("bpy.data.objects[Cube] as obj and str = ", attr_str)
# action_type, action, prop, path_attr = attr_get_type(
#    bpy.data.objects["Cube"], attr_str
# )
# print("OUTPUTS ===== ")
# print("type(action) = ", action_type)
# print("action = ", action)
# print("prop = ", prop)
# print("path_attr = ", path_attr)


def get_attr_only_str(full_str):
    if "data" in full_str:
        mod = 0
    elif "[" in full_str:
        mod = 1
    else:
        mod = 0

    len_path = len(full_str.rsplit(".", 100)) - mod
    print("len_path = ", len_path)

    list_parent_nodes_str = full_str.rsplit(".", len_path - 3)
    print("list_parent_nodes_str = ", list_parent_nodes_str)

    attribute_only_str = full_str.replace(list_parent_nodes_str[0] + ".", "")

    return attribute_only_str


full_str = "bpy.context.scene.objects['Cube'].collision.absorption"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)

# full_str='bpy.context.scene.camera.location'
# attr_only_str=get_attr_only_str(full_str)
# print('attr_only_str = ', attr_only_str)


def attr_set_val(obj, path, min_val, max_val, UD_type):
    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
        # len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS))
        path_prop, path_attr = path.rsplit(".", 1)

        # same as: prop = obj.modifiers["Subsurf"]
        prop = obj.path_resolve(path_prop)
    else:
        prop = obj
        # single attribute such as name, location... etc
        path_attr = path

    # same as: prop.levels = value

    try:
        getattr(prop, path_attr)
    except Exception:
        # print("Property does not exist")
        pass
    # action = getattr(prop, path_attr)

    print("attr_set_val type ========================= ", UD_type)
    # if UD_type==float:
    #     min_array = np.array(getattr(self, "min_" + m_str))
    #     max_array = np.array(getattr(self, "max_" + m_str))

    if UD_type == float:
        print("HELLO 1D FLOAT!!!!!!!")
        # if rand_posx:
        #     getattr(context.scene.camera, value_str)[0] = uniform(
        #         loc_x_range[0], loc_x_range[1]
        #     )

        # if rand_rotz:
        #     rand_z = uniform(rot_z_range[0], rot_z_range[1])
        # else:
        #     rand_z = uniform(0.0, 0.0)

        # vec = Vector([rand_x, rand_y, rand_z])

        # bpy.data.objects["Camera"].rotation_euler[0] = vec[0]

        value = random.uniform(min_val, max_val)
        print(value)
    elif UD_type == Vector:
        print("HELLO 3D VECTOR FLOAT!!!!!")
        value = random.uniform(min_val, max_val)
        print(value)
    else:
        print("HELLO INTEGER!!!!!!!!!!!!!!!!!!!!")
        value = random.randint(min_val, max_val)
        print(value)

    setattr(prop, path_attr, value)


#### camera.location
full_str = "bpy.context.scene.camera.location"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)

path_prop, path_attr = "camera.location".rsplit(".", 1)
prop = bpy.context.scene.path_resolve(path_prop)
action = getattr(prop, path_attr)
print("prop = ", prop)
print("action getattr = ", action)

prop_type, action, prop, path_attr = attr_get_type(
    bpy.context.scene, attr_only_str
)

min_val = np.array(
    getattr(
        bpy.context.scene.socket_props_per_UD.collection[0],
        "min_float_3d",
    )
)

max_val = np.array(
    getattr(
        bpy.context.scene.socket_props_per_UD.collection[0],
        "max_float_3d",
    )
)
print(min_val)
print(max_val)
print(prop_type)
# min_val = bpy.context.scene.socket_props_per_UD.collection[0].min_float_1d[0]
# max_val = bpy.context.scene.socket_props_per_UD.collection[0].max_float_1d[0]
attr_set_val(
    bpy.context.scene,
    attr_only_str,
    min_val,
    max_val,
    prop_type,
)


#### frame_current
full_str = "bpy.context.scene.frame_current"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)

prop = bpy.context.scene
# single attribute such as name, location... etc
path_attr = "frame_current"
action = getattr(prop, path_attr)
print("prop = ", prop)
print("action getattr = ", action)

prop_type, action, prop, path_attr = attr_get_type(
    bpy.context.scene, attr_only_str
)

min_val = np.array(
    getattr(
        bpy.context.scene.socket_props_per_UD.collection[1],
        "min_int_1d",
    )
)

max_val = np.array(
    getattr(
        bpy.context.scene.socket_props_per_UD.collection[1],
        "max_int_1d",
    )
)
print(min_val)
print(max_val)
print(prop_type)
# min_val = bpy.context.scene.socket_props_per_UD.collection[0].min_float_1d[0]
# max_val = bpy.context.scene.socket_props_per_UD.collection[0].max_float_1d[0]
attr_set_val(
    bpy.context.scene,
    attr_only_str,
    min_val,
    max_val,
    prop_type,
)

#### collision.absorption
full_str = "bpy.context.scene.objects['Cube'].collision.absorption"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)

path_prop, path_attr = "collision.absorption".rsplit(".", 1)
prop = bpy.context.scene.objects["Cube"].path_resolve(path_prop)
action = getattr(prop, path_attr)
print("prop = ", prop)
print("action getattr = ", action)

prop_type, action, prop, path_attr = attr_get_type(
    bpy.data.objects["Cube"], attr_only_str
)


min_val = getattr(
    bpy.context.scene.socket_props_per_UD.collection[2],
    "min_float_1d",
)


max_val = np.array(
    getattr(
        bpy.context.scene.socket_props_per_UD.collection[2],
        "max_float_1d",
    )
)
print(min_val)
print(max_val)
print(prop_type)

objects_in_scene = []
for i, key in enumerate(bpy.data.objects):
    print(i)
    print(key.name)
    objects_in_scene.append(key.name)


if "[" in full_str:
    # obj=bpy.data.objects.get(fiinal)
    obj_str = get_obj_str(full_str)

    print("obj_str = ", obj_str)
    for i, obj in enumerate(objects_in_scene):
        print(obj)
        print(i)
        #        regex=re.compile(r'^test-\d+$')

        if obj in obj_str:
            print("Yay found cube")
            print(i)
            idx = i

    attr_set_val(
        bpy.data.objects[idx],
        attr_only_str,
        min_val,
        max_val,
        prop_type,
    )


####Tom examples -  bpy.data.objects["Cube"].location[0]
# bpy.data.objects["Cube"].rotation_euler
full_str = "bpy.data.cameras['Camera'].dof.aperture_fstop"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)


path_prop, path_attr = "dof.aperture_fstop".rsplit(".", 1)
prop = bpy.data.cameras["Camera"].path_resolve(path_prop)
action = getattr(prop, path_attr)
print("prop = ", prop)
print("action getattr = ", action)

prop_type, action, prop, path_attr = attr_get_type(
    bpy.data.cameras["Camera"], attr_only_str
)


full_str = "bpy.data.objects['Cube'].location[0]"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)


path_prop = "location"
path_attr = "location[0]"
prop = bpy.data.objects[1].path_resolve("location")
print(prop)
action = prop[0]
# print("prop = ", prop)
# print("action getattr = ", action)


attr_type = attr_get_type(bpy.data.objects[idx], attr_only_str)[0]

print("attr_type", attr_type)

# min_val = np.array(
#    getattr(
#        bpy.context.scene.socket_props_per_UD.collection[0],
#        "min_float_3d",
#    )
# )

# max_val = np.array(
#    getattr(
#        bpy.context.scene.socket_props_per_UD.collection[0],
#        "max_float_3d",
#    )
# )
# print(min_val)
# print(max_val)
# print(prop_type)
## min_val = bpy.context.scene.socket_props_per_UD.
# collection[0].min_float_1d[0]
## max_val = bpy.context.scene.socket_props_per_UD.
# collection[0].max_float_1d[0]
# attr_set_val(
#    bpy.context.scene,
#    attr_only_str,
#    min_val,
#    max_val,
#    prop_type,
# )

# import re
# objects_in_scene=[]
# for i, key in enumerate(bpy.data.objects):
#    # print(i)
#    # print(key.name)
#    objects_in_scene.append(key.name)

# UD_name = "bpy.data.objects['Cube'].location[0]"
# print("ERROR ======= UD.name", UD_name)
# tmp_attr = get_attr_only_str(UD_name)
# print("ERROR ======== attr_str", tmp_attr)
# a = re.findall('\[(.*?)\]', tmp_attr)
# if a:
#    nums = list(map(int, a[0].split(',')))
#    print(nums)
#    print(type(str(nums[0])))
# else:
#    nums = []
#
# print("len", len(nums))

# if len(nums)>0:
#    print('Number is ', nums)
#    print('type(Number) is ', type(nums[0]))
#
#    num_str=str(nums[0])
#
#    attribute_only_str = tmp_attr.replace("[" + num_str + "]", "")
#
#    print("new_UD_name", attribute_only_str)
#
#    obj_str = get_obj_str(UD_name)
#    print("obj_str", obj_str)
#
#
# else:
#    obj_str = get_obj_str(UD_name)
#    print("obj_str", obj_str)
#
# for i, obj in enumerate(objects_in_scene):
#        #        regex=re.compile(r'^test-\d+$')

#    if obj in obj_str:
#        current_obj = obj
#        print("Found ", current_obj)
#        idx = i

# print("location[0]??????", current_obj)
# %%
