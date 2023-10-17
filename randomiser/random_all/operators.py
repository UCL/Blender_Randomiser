import datetime
import json
from random import seed

import bpy
import numpy as np
from bpy.app.handlers import persistent

from ..transform.operators import get_transform_inputs, randomise_selected
from ..utils import nodes2rand


# -------------------------------
# Operator
# -------------------------------
class ApplyRandomAll(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Randomise all the panels

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.randomise_all"  # appended to bpy.ops.
    bl_label = "Apply randomisation to all panels"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the randomiser operator

        Randomise all the panels

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        (
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        ) = get_transform_inputs(context)

        randomise_selected(
            context,
            loc,
            loc_x_range,
            loc_y_range,
            loc_z_range,
            rot,
            rot_x_range,
            rot_y_range,
            rot_z_range,
            delta_on,
            rand_posx,
            rand_posy,
            rand_posz,
            rand_rotx,
            rand_roty,
            rand_rotz,
        )

        return {"FINISHED"}


# -------------------------------
class ApplySaveParams(bpy.types.Operator):
    # docstring shows as a tooltip for menu items and buttons.
    """Save parameter outputs in .json

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "camera.save_param_out"  # appended to bpy.ops.
    bl_label = "Save parameter outputs"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        """Execute the save param operator

        Randomise camera transforms, materials and geometry
        for selected number of frames and save output parameters
        in .json

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        ### ALL
        if bpy.data.scenes["Scene"].seed_properties.seed_toggle:  # = True
            seed(bpy.data.scenes["Scene"].seed_properties.seed)
        tot_frame_no = bpy.context.scene.rand_all_properties.tot_frame_no

        ### TRANSFORMS
        bpy.data.scenes["Scene"].frame_current = 0

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

        rad2deg = 180 / np.pi
        for idx in range(tot_frame_no):
            bpy.app.handlers.frame_change_pre[0]("dummy")
            bpy.data.scenes["Scene"].frame_current = idx

            x_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[0]
            )
            y_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[1]
            )
            z_pos_vals.append(
                getattr(bpy.context.scene.camera, loc_value_str)[2]
            )

            x_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[0] * rad2deg
            )
            y_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[1] * rad2deg
            )
            z_rot_vals.append(
                getattr(bpy.context.scene.camera, value_str)[2] * rad2deg
            )

        ### GEOMETRY
        bpy.data.scenes["Scene"].frame_current = 0

        all_geom_dict = {}
        cs = bpy.context.scene
        for gng_idx in range(len(cs.socket_props_per_gng.collection)):
            # get this subpanel's GNG
            subpanel_gng = cs.socket_props_per_gng.collection[gng_idx]
            tmp_GNG = subpanel_gng.name
            print(tmp_GNG)

            sockets_props_collection = cs.socket_props_per_gng.collection[
                subpanel_gng.name
            ].collection

            list_parent_nodes_str = [
                sckt.name.split("_")[0] for sckt in sockets_props_collection
            ]
            list_input_nodes = [
                bpy.data.node_groups[subpanel_gng.name].nodes[nd_str]
                for nd_str in list_parent_nodes_str
            ]

            list_input_nodes_sorted = sorted(
                list_input_nodes, key=lambda x: x.name
            )
            for i_n, nd in enumerate(list_input_nodes_sorted):
                # add sockets for this node in the subseq rows
                for sckt in nd.outputs:
                    print("i_n", i_n)
                    print("nd", nd)
                    print(
                        getattr(
                            sckt,
                            "default_value",
                        )
                    )

                    tmp_values = []
                    for idx in range(tot_frame_no):
                        bpy.app.handlers.frame_change_pre[0]("dummy")
                        bpy.data.scenes["Scene"].frame_current = idx
                        bpy.ops.node.randomise_all_geometry_sockets(
                            "INVOKE_DEFAULT"
                        )  # issue
                        # w/ this being called so often -
                        # might need moved to diff for loop?
                        tmp_values.append(
                            getattr(
                                sckt,
                                "default_value",
                            )
                        )

                    print(tmp_values)
                    tmp_sck = nd.name
                    # all_geom_dict[tmp_GNG] = tmp_sck
                    GNG_sck_values_str = tmp_GNG + tmp_sck
                    GNG_sck_values_str = "Values " + GNG_sck_values_str
                    print(GNG_sck_values_str)
                    all_geom_dict[GNG_sck_values_str] = tmp_values

        print(all_geom_dict)

        ### MATERIALS
        bpy.data.scenes["Scene"].frame_current = 0
        all_mat_dict = {}
        cs = bpy.context.scene
        for mat_idx in range(len(cs.socket_props_per_material.collection)):
            # get this subpanel's GNG
            subpanel_material = cs.socket_props_per_material.collection[
                mat_idx
            ]
            tmp_mat = subpanel_material.name
            print(tmp_mat)

            list_input_nodes = (
                nodes2rand.get_material_nodes_to_randomise_indep(
                    subpanel_material.name
                )
            )

            list_nodes2rand_in_groups = (
                nodes2rand.get_material_nodes_to_randomise_group(
                    subpanel_material.name
                )
            )

            list_input_nodes_all = (
                nodes2rand.get_material_nodes_to_randomise_all(
                    subpanel_material.name
                )
            )

            print("list_input_nodes ====== ", list_input_nodes)
            print(
                "list nodes2rand in groups ===== ", list_nodes2rand_in_groups
            )
            print("list_input_nodes_all ===== ", list_input_nodes_all)

            list_input_nodes_sorted = sorted(
                list_input_nodes_all, key=lambda x: x.name
            )
            for i_n, nd in enumerate(list_input_nodes_sorted):
                # add sockets for this node in the subseq rows
                print("nd.name", nd.name)
                for sckt in nd.outputs:
                    print(nd.name)
                    print(
                        getattr(
                            sckt,
                            "default_value",
                        )
                    )

                    test_attr = getattr(
                        sckt,
                        "default_value",
                    )
                    print(str(test_attr))

                    if "NodeSocketColor" not in str(test_attr):
                        print("NODESOCKETCOLOR", str(test_attr))
                        tmp_values = []
                        for idx in range(tot_frame_no):
                            bpy.app.handlers.frame_change_pre[0]("dummy")
                            bpy.data.scenes["Scene"].frame_current = idx
                            bpy.ops.node.randomise_all_material_sockets(
                                "INVOKE_DEFAULT"
                            )  # issue
                            # w/ this being called so often -
                            # might need moved to diff for loop?
                            tmp_values.append(
                                getattr(
                                    sckt,
                                    "default_value",
                                )
                            )

                        print(tmp_values)
                        tmp_sck = nd.name
                        # all_mat_dict[tmp_mat] = tmp_sck
                        if (
                            list_input_nodes_sorted[i_n]
                            in list_nodes2rand_in_groups
                        ):
                            for ng in bpy.data.node_groups:
                                print("ng in bpy.data.node_groups", ng.name)
                                MAT_sck_values_str = (
                                    tmp_mat + ng.name + tmp_sck
                                )

                        else:
                            MAT_sck_values_str = tmp_mat + tmp_sck

                        MAT_sck_values_str = "Values " + MAT_sck_values_str
                        print(MAT_sck_values_str)
                        all_mat_dict[MAT_sck_values_str] = tmp_values

        print(all_mat_dict)
        data = {
            "location_str": loc_value_str,
            "loc_x": x_pos_vals,
            "loc_y": y_pos_vals,
            "loc_z": z_pos_vals,
            "rotation_str": value_str,
            "rot_x": x_rot_vals,
            "rot_y": y_rot_vals,
            "rot_z": z_rot_vals,
            "geometry": all_geom_dict,
            "materials": all_mat_dict,
        }

        ct = datetime.datetime.now()
        ts = ct.timestamp()
        ts_str = str(ts)
        file_ext = ".json"
        path_to_file = "output_randomisations_per_frame" + ts_str
        path_to_file = path_to_file + file_ext

        with open(path_to_file, "w") as out_file_obj:
            # convert the dictionary into text
            text = json.dumps(data, indent=4)
            # write the text into the file
            out_file_obj.write(text)

        return {"FINISHED"}


@persistent
def randomise_all_per_frame(dummy):
    bpy.ops.camera.randomise_all("INVOKE_DEFAULT")

    return


# ---------------------
# Classes to register
# ---------------------
list_classes_to_register = [
    ApplyRandomAll,
    ApplySaveParams,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    bpy.app.handlers.frame_change_pre.append(randomise_all_per_frame)

    print("randomise all operators registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.frame_change_pre.remove(randomise_all_per_frame)

    print("randomise all unregistered")
