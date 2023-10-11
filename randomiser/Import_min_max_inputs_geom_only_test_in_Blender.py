import json
import re

import bpy

out_path_to_file = "./transform_geom_mat_test.json"
with open(out_path_to_file, "r") as in_file_obj:
    text = in_file_obj.read()
    # convert the text into a dictionary
    out_data = json.loads(text)

print(out_data["geometry"])

geom_out_dict = out_data["geometry"]

counter_dict = 0
for n, keys in geom_out_dict.items():
    #    print(n)
    #    print(keys)
    counter_dict = +counter_dict
    if "Values" in str(keys):
        print("ONLY NEEDED n ", n)
        print("ONLY NEEDED keys ", keys)

for obj in bpy.data.objects:
    if "Cube" in str(obj):
        active_obj = obj
    elif "Sphere" in str(obj):
        active_obj = obj
# obj = bpy.data.objects[3] #Sphere
bpy.context.view_layer.objects.active = obj
bpy.context.scene.socket_props_per_gng.update_gngs_collection
bpy.ops.node.randomise_all_geometry_sockets("INVOKE_DEFAULT")

## set range for randomise in blender properties
# bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
#    0
# ].max_float_1d[0] = upper_bound
# bpy.data.scenes["Scene"].socket_props_per_gng.collection[0].collection[
#    0
# ].min_float_1d[0] = lower_bound

#### GEOMETRY
# bpy.data.scenes["Scene"].frame_current = 0

### GEOMETRY
# collection[N].collection[S]
# [N] = 0, 1, 2 for each node group (even NG within NG)
# [S] = 0, 1 etc. for each socket within node group
# Actual Geom values followed by Min_Max
# Node group called "Geometry Nodes"

all_geom_dict = {}
cs = bpy.context.scene

counter = 0
all_geom_dict["min"] = 1
all_geom_dict["max"] = 5
for gng_idx in range(len(cs.socket_props_per_gng.collection)):
    # for gng in cs.socket_props_per_gng.collection:

    # get this subpanel's GNG
    subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]
    print(subpanel_gng.name)

    cs.socket_props_per_gng.collection[subpanel_gng.name].update_input_json

    # force an update in the sockets for this GNG
    cs.socket_props_per_gng.collection[
        subpanel_gng.name
    ].update_sockets_collection
    print("TEST Collection of Geometry Node Groups updated")

    sckt_prop = subpanel_gng.collection

    for sckt in subpanel_gng.collection:
        #        geom_current = {}
        print("sckt in sckt_prop = ", sckt)
        print(type(sckt))
        tmp_sck = sckt.name
        print(sckt.name)

        #        if "_Value" in tmp_sck:
        #            tmp_sck=tmp_sck.replace("_Value", "")
        #            print(tmp_sck)
        #        print(type(tmp_sck))

        #        sckt_cand = subpanel_gng.candidate_sockets
        #
        for s in subpanel_gng.candidate_sockets:
            # build socket id from scratch
            socket_id = s.node.name + "_" + s.name
            print("socket_id ===== ")
            print(socket_id)

            if socket_id == tmp_sck:
                sckt_val = s
                break

        # for this socket type, get the name of the attribute
        # holding the min/max properties
        socket_attrib_str = bpy.context.scene.socket_type_to_attr[
            type(sckt_val)
        ]

        # extract last number between '_' and 'd/D' in the
        # attribute name, to determine the shape of the array
        # TODO: there is probably a nicer way to do this...
        n_dim = int(re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1])
        # ---------------------------

        # get dictionary with initial min/max values
        # for this socket type
        #        ini_min_max_values = (
        #            bpy.context.scene.socket_type_to_ini_min_max[type(sckt_val)]
        #        )

        ini_min_max_values = all_geom_dict

        print(ini_min_max_values)
        print(sckt_prop)
        print(socket_attrib_str)
        print(n_dim)

        # assign initial value
        for m_str in ["min", "max"]:
            setattr(
                sckt,  # sckt_prop,
                m_str + "_" + socket_attrib_str,
                (ini_min_max_values[m_str],) * n_dim,
            )

    #### CODE HAPPENS AFTER INITIAL VALUES SET SO NOT NEEDED?
#    # get (updated) collection of socket props for this GNG
#    sockets_props_collection = cs.socket_props_per_gng.collection[
#        subpanel_gng.name
#    ].collection
#    print(sockets_props_collection)


#    list_parent_nodes_str = [
#        sckt.name.split("_")[0] for sckt in sockets_props_collection
#    ]
#    list_input_nodes = [
#        bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
#        for nd_str in list_parent_nodes_str
#    ]

#    list_input_nodes_sorted = sorted(
#        list_input_nodes, key=lambda x: x.name
#    )


##    # if socket is not color type: format as a regular property
##    else:
##        for m_str in zip(["min", "max"]):
###            bpy.data.scenes["Scene"].socket_props_per_gng.
# collection[0].collection[
###    0
###].max_float_1d[0]
##            sockets_props_collection[socket_id]
##            col.prop(
##                sockets_props_collection[socket_id],
##                m_str + "_" + cs.socket_type_to_attr[type(sckt)],
##                icon_only=True,
##            )
#
#    for i_n, nd in enumerate(list_input_nodes_sorted):
#        # add sockets for this node in the subseq rows
#        for sckt in nd.outputs:
#            print("i_n", i_n)
#            print("nd", nd)
#            print(
#                getattr(
#                    sckt,
#                    "default_value",
#                )
#            )

# for gng_idx in range(len(cs.socket_props_per_gng.collection)):
#    # get this subpanel's GNG
#    subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]
#    tmp_GNG = subpanel_gng.name
#    print(tmp_GNG)

#    sockets_props_collection = cs.socket_props_per_gng.collection[
#        subpanel_gng.name
#    ].collection

#    list_parent_nodes_str = [
#        sckt.name.split("_")[0] for sckt in sockets_props_collection
#    ]
#    list_input_nodes = [
#        bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
#        for nd_str in list_parent_nodes_str
#    ]

#    list_input_nodes_sorted = sorted(
#        list_input_nodes, key=lambda x: x.name
#    )
#    for i_n, nd in enumerate(list_input_nodes_sorted):
#        # add sockets for this node in the subseq rows
#        for sckt in nd.outputs:
#            print("i_n", i_n)
#            print("nd", nd)
#            print(
#                getattr(
#                    sckt,
#                    "default_value",
#                )
#            )

#            tmp_values = []
#            for idx in range(tot_frame_no):
#                bpy.app.handlers.frame_change_pre[0]("dummy")
#                bpy.data.scenes["Scene"].frame_current = idx
#                bpy.ops.node.randomise_all_geometry_sockets(
#                    "INVOKE_DEFAULT"
#                )  # issue
#                # w/ this being called so often -
#                # might need moved to diff for loop?
#                tmp_values.append(
#                    getattr(
#                        sckt,
#                        "default_value",
#                    )
#                )

#            print(tmp_values)
#            tmp_sck = nd.name
#            all_geom_dict[tmp_GNG] = tmp_sck
#            GNG_sck_values_str = tmp_GNG + tmp_sck
#            GNG_sck_values_str = "Values " + GNG_sck_values_str
#            print(GNG_sck_values_str)
#            all_geom_dict[GNG_sck_values_str] = tmp_values
