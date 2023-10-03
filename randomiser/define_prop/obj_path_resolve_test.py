import random

import bpy
import numpy as np

# from random import random
from mathutils import Vector

# %%
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

# %%


def attr_get_type(obj, path):
    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
        # len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS))
        path_prop, path_attr = path.rsplit(".", 1)

        print("if statement ==== ")
        print(
            "FROM rsplit . path_prop for resolve = ",
            path_prop,
            " and path_attr  for getattr = ",
            path_attr,
        )
        print("obj used for path_resolve = ", obj)

        # same as: prop = obj.modifiers["Subsurf"]
        prop = obj.path_resolve(path_prop)
        print("prop from path_resolve  for get_attr = ", prop)
    else:
        print("else statement ==== ")
        prop = obj
        print("prop = obj ", prop)
        # single attribute such as name, location... etc
        path_attr = path
        print("path_attr = path ", path_attr)

    # same as: prop.levels = value

    try:
        action = getattr(prop, path_attr)
    except Exception:
        # print("Property does not exist")
        action = "dummy"
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

attr_set_val(
    bpy.data.objects["Cube"],
    attr_only_str,
    min_val,
    max_val,
    prop_type,
)
