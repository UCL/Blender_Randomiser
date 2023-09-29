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
    if "[" in full_str:
        len_path = len(full_str.rsplit(".", 100)) - 1
        print("len_path = ", len_path)
        list_parent_nodes_str = full_str.rsplit(".", len_path - 3)
        print("list_parent_nodes_str = ", list_parent_nodes_str)
        attribute_only_str = full_str.replace(
            list_parent_nodes_str[0] + ".", ""
        )
    else:
        len_path = len(full_str.rsplit(".", 100))
        print("len_path = ", len_path)
        list_parent_nodes_str = full_str.rsplit(".", len_path - 3)
        print("list_parent_nodes_str = ", list_parent_nodes_str)
        attribute_only_str = full_str.replace(
            list_parent_nodes_str[0] + ".", ""
        )

    return attribute_only_str


full_str = "bpy.context.scene.objects['Cube'].collision.absorption"
attr_only_str = get_attr_only_str(full_str)
print("attr_only_str = ", attr_only_str)

# full_str='bpy.context.scene.camera.location'
# attr_only_str=get_attr_only_str(full_str)
# print('attr_only_str = ', attr_only_str)
