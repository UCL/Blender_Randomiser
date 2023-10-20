import bpy


def mat_list_to_rand(cs):
    list_subpanel_material_names = [
        mat.name
        for mat in cs.socket_props_per_material.collection
        # for mat in cs.socket_props_per_material.candidate_materials
    ]

    # for every material: save sockets to randomise
    sockets_to_randomise_per_material = {}
    for mat_str in list_subpanel_material_names:
        # get collection of socket properties for this material
        # ATT socket properties do not include the actual socket object
        if cs.socket_props_per_material.collection[
            mat_str
        ].update_sockets_collection:
            print("Collection of material sockets updated")

        sockets_props_collection = cs.socket_props_per_material.collection[
            mat_str
        ].collection

        # get candidate sockets for this material
        candidate_sockets = cs.socket_props_per_material.collection[
            mat_str
        ].candidate_sockets

        # if socket unlinked and randomisation toggle is True:
        # modify socket props to set toggle to False
        sockets_to_randomise_per_material[mat_str] = []
        for sckt in candidate_sockets:
            # get socket identifier sting
            sckt_id = sckt.node.name + "_" + sckt.name
            if sckt.node.id_data.name in bpy.data.node_groups:
                sckt_id = sckt.node.id_data.name + "_" + sckt_id

            # if this socket is selected to randomise but it is unlinked:
            # set randomisation toggle to False
            if (not sckt.is_linked) and (
                sockets_props_collection[sckt_id].bool_randomise
            ):
                setattr(
                    sockets_props_collection[sckt_id],
                    "bool_randomise",
                    False,
                )
                print(
                    f"Socket {sckt_id} from {mat_str} is unlinked:",
                    "randomisation toggle set to False",
                )

            # after modifying randomisation toggle
            # save list of sockets to randomise to dict,
            # with key = material
            if sockets_props_collection[sckt_id].bool_randomise:
                sockets_to_randomise_per_material[mat_str].append(sckt)

    return list_subpanel_material_names, sockets_to_randomise_per_material


def geom_list_to_rand(cs):
    list_subpanel_gng_names = [
        gng.name for gng in cs.socket_props_per_gng.collection
    ]
    # for every GNG: save sockets to randomise
    sockets_to_randomise_per_gng = {}
    for gng_str in list_subpanel_gng_names:
        # get collection of socket properties for this GNG
        # ATT socket properties do not include the actual socket object
        if cs.socket_props_per_gng.collection[
            gng_str
        ].update_sockets_collection:
            print("Collection of geometry sockets updated")

        sockets_props_collection = cs.socket_props_per_gng.collection[
            gng_str
        ].collection

        # get candidate sockets for this GNG
        candidate_sockets = cs.socket_props_per_gng.collection[
            gng_str
        ].candidate_sockets

        # if socket unlinked and randomisation toggle is True:
        # modify socket props to set toggle to False
        sockets_to_randomise_per_gng[gng_str] = []
        for sckt in candidate_sockets:
            # get socket identifier string
            sckt_id = sckt.node.name + "_" + sckt.name

            # if this socket is selected to randomise but it is unlinked:
            # set randomisation toggle to False
            if (not sckt.is_linked) and (
                sockets_props_collection[sckt_id].bool_randomise
            ):
                setattr(
                    sockets_props_collection[sckt_id],
                    "bool_randomise",
                    False,
                )
                print(
                    f"Socket {sckt_id} from {gng_str} is unlinked:",
                    "randomisation toggle set to False",
                )

            # after modifying randomisation toggle
            # save list of sockets to randomise to dict,
            # with key = material
            if sockets_props_collection[sckt_id].bool_randomise:
                sockets_to_randomise_per_gng[gng_str].append(sckt)

    return sockets_to_randomise_per_gng
