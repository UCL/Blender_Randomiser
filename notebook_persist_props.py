"""Persist socket properties when we switch material

Until I autopopulate materials higher level collection:
>>> mat =  bpy.context.scene.socket_props_per_material.add()
>>> mat.name='Material'
>>> mat =  bpy.context.scene.socket_props_per_material.add()
>>> mat.name='Material.001'


-----------
To test: I created three materials with 1,2 and 3 input nodes
'RandomValue.xxx' respectively

Add materials (manually for now)
>>> mat=bpy.context.scene.socket_props_per_material.add()
>>> mat.name='Material'
>>> mat=bpy.context.scene.socket_props_per_material.add()
>>> mat.name='Material.001'
>>> mat=bpy.context.scene.socket_props_per_material.add()
>>> mat.name='Material.002'
>>> len(bpy.context.scene.socket_props_per_material)
3

Check names
>>> [mat.name for mat in bpy.context.scene.socket_props_per_material]
['Material', 'Material.001', 'Material.002']

Check length of collection of socket properties
>>> [len(mat.collection) for mat in
bpy.context.scene.socket_props_per_material]
[0, 0, 0]

Update collection of socket props if required
>>> [mat.update_collection for mat in
bpy.context.scene.socket_props_per_material]
Collection of sockets updated
Collection of sockets updated
Collection of sockets updated
[True, True, True]

Check length of socket props
>>> [len(mat.collection) for mat in
bpy.context.scene.socket_props_per_material]
[1, 2, 3]

"""


import re

import bpy
import numpy as np

MAP_SOCKET_TYPE_TO_ATTR = {
    bpy.types.NodeSocketFloat: "float_1d",
    bpy.types.NodeSocketVector: "float_3d",
    bpy.types.NodeSocketColor: "rgba_4d",  # "float_4d",
}

# NOTE: if the property is a float vector of size (1,n)
# the initial min/max values specified here apply to all n dimensions
# TODO: should we change this to allow different values per dimension?
# (in that case the mapping should probably be from attribute name)
MAP_SOCKET_TYPE_TO_INI_MIN_MAX = {
    bpy.types.NodeSocketFloat: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketVector: {"min": -np.inf, "max": np.inf},
    bpy.types.NodeSocketColor: {"min": 0.0, "max": 1.0},
}


# ------------------------------------
# ColSocketProperties
# ------------------------------------
def get_update_collection(self):
    """Get function for the update_collection attribute
    of the class ColSocketProperties

    It will run when the property value is 'get' and
    it will update the collection of socket properties if required

    Returns
    -------
    boolean
        returns True if the collection of socket properties is updated,
        otherwise it returns False
    """

    # set of sockets in collection for this material
    # assign to self-----
    self.set_sckt_names_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # ----------------------
    # set of sockets in graph *for this material* !
    # can I save candidate_sockets as an attrib? (using property()?)
    # assign to self-----
    self.set_sckt_names_in_graph = set(
        sck.node.name + "_" + sck.name for sck in self.candidate_sockets
    )
    # ----------------------

    # set of sockets that are just in one of the two groups
    # assign to self-----
    self.set_of_sckt_names_in_one_only = (
        self.set_sckt_names_in_collection_of_props.symmetric_difference(
            self.set_sckt_names_in_graph
        )
    )

    # if there is a difference:
    # edit the collection of sockets
    # with the latest data
    if self.set_of_sckt_names_in_one_only:
        set_update_collection(self, True)
        return True  # if returns True, it has been updated
    else:
        return False  # if returns False, it hasn't


def set_update_collection(self, value):
    """Set function for the update_collection attribute
    of the class ColSocketProperties.

    It will run when the property value is 'set'
    It will overwrite the collection of socket properties

    Parameters
    ----------
    value : boolean
        if True, the collection of socket properties is
        overwritten to consider the latest data
    """

    if value:
        # for the set of sockets that exist only in one of the sets:
        # - if the socket exists only in the collection: remove from collection
        # - if the socket exists only in the node graph: add to collection with
        #  initial values
        # for the rest of sockets: leave untouched
        print("Difference between collection and graph")
        print(f"Sockets in one set only:{self.set_of_sckt_names_in_one_only}")

        for sckt_name in self.set_of_sckt_names_in_one_only:
            # - if the socket exists only in the collection: remove from
            # collection
            if sckt_name in self.set_sckt_names_in_collection_of_props:
                print(f"{sckt_name} existed only in collection: removed")
                print(f"Length collection before: {len(self.collection)}")
                self.collection.remove(self.collection.find(sckt_name))
                print(f"Length collection after: {len(self.collection)}")
            # - if the socket exists only in the node graph: add to collection
            # with initial values
            if sckt_name in self.set_sckt_names_in_graph:
                sckt_prop = self.collection.add()
                sckt_prop.name = sckt_name
                sckt_prop.bool_randomise = True

                # ---------------------------
                print([s.name for s in self.candidate_sockets])
                # get socket object for this socket name
                # NOTE: my definition of socket name
                # (node.name + _ + socket.name)
                sckt = [
                    s
                    for s in self.candidate_sockets
                    if s.node.name + "_" + s.name == sckt_name
                ][0]

                # add min/max values
                # TODO: review - is this too hacky?
                # for this socket type, get the name of the attribute
                # holding the min/max properties
                socket_attrib_str = bpy.context.scene.socket_type_to_attr[
                    type(sckt)
                ]
                # for the shape of the array from the attribute name:
                # extract last number between '_' and 'd/D' in the attribute
                # name
                n_dim = int(
                    re.findall(r"_(\d+)(?:d|D)", socket_attrib_str)[-1]
                )
                # ---------------------------

                # get dict with initial min/max values for this socket type
                ini_min_max_values = (
                    bpy.context.scene.socket_type_to_ini_min_max[type(sckt)]
                )

                # assign initial value ----only if
                for m_str in ["min", "max"]:
                    setattr(
                        sckt_prop,
                        m_str + "_" + socket_attrib_str,
                        (ini_min_max_values[m_str],) * n_dim,
                    )

        # ----------------
        # # returns ID of the element with that name
        # self.collection.find('RandomValue.002_Value')
        # # remove those no longer in graph (by ID)
        # self.collection.remove(self.collection.find('RandomValue.002_Value'))
        # ------
        #


# --------------------------
class SocketProperties(bpy.types.PropertyGroup):
    # name (we can use it to access sockets in collection by name)
    name: bpy.props.StringProperty()  # type: ignore

    min_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore
    max_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore

    min_float_3d: bpy.props.FloatVectorProperty(size=3)  # type: ignore
    max_float_3d: bpy.props.FloatVectorProperty(size=3)  # type: ignore

    min_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore
    max_float_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore

    min_rgba_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore
    max_rgba_4d: bpy.props.FloatVectorProperty(size=4)  # type: ignore

    ### bool
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


class ColSocketProperties(bpy.types.PropertyGroup):
    # can I use this to hold the name of the material?
    name: bpy.props.StringProperty()  # type: ignore

    # collection of socket props
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # 'dummy' attribute to update collection
    # if I do :
    # bpy.context.scene.socket_props_per_material['Material'].update_collection
    #  --> it will check
    # and update the collection if required
    update_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_collection,
        set=set_update_collection,
    )

    # --------------------------------
    # TODO : can I use decorator instead?
    def get_candidate_sockets(self):
        list_input_nodes = [
            nd
            for nd in bpy.data.materials[self.name].node_tree.nodes
            if len(nd.inputs) == 0
            and nd.name.lower().startswith("random".lower())
        ]

        # list of sockets
        # TODO: should we exclude unlinked ones here instead?
        list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
        return list_sockets

    candidate_sockets = property(fget=get_candidate_sockets)
    # ---------------


# class ColMaterials(bpy.types.PropertyGroup):
#     collection: bpy.props.CollectionProperty(  # type: ignore
#         type=ColSocketProperties
#     )

#     update_collection


# ------------------------------------
# Panel
class SamplePanel(bpy.types.Panel):
    """Class defining the panel for randomising
    material node properties

    """

    # TODO: are these docstrings shown in the UI as tooltips somewhere?

    # metadata
    bl_idname = "NODE_MATERIAL_PT_random"
    bl_label = "Randomise MATERIAL"  # title of the panel displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        # draw the panel only if there is an active material
        # for the selected object
        return context.object.active_material is not None

    def draw(self, context):
        # Get list of input nodes to randomise
        # for currently active material
        # list_input_nodes = utils.get_material_input_nodes_to_randomise(
        #     context.object.active_material.name
        # )
        list_input_nodes = [
            nd
            for nd in bpy.data.materials[
                context.object.active_material.name
            ].node_tree.nodes
            if len(nd.inputs) == 0
            and nd.name.lower().startswith("random".lower())
        ]

        # ------------------------------------------------------
        # If collection for this material hasn't been defined: add now
        # TODO: should I add somewhere else (use update attribute?)
        # ----yes because I cant write to ID classes in this context
        # cs = context.scene
        # if cs.socket_props_per_material.find(
        #     context.object.active_material.name
        # ) == -1:
        #     mat = cs.socket_props_per_material.add()
        #     mat.name = context.object.active_material.name
        # ------------------------------------------------------

        # Get collection of sockets' properties
        # 'context.scene.sockets2randomise_props.update_collection'
        # triggers the get function that checks if an update is
        # required. If it is, the collection of sockets is updated
        # and 'context.scene.sockets2randomise_props.update_collection'
        # returns TRUE
        cs = context.scene
        if cs.socket_props_per_material[
            context.object.active_material.name
        ].update_collection:
            print("Collection of sockets updated")
        sockets_props_collection = cs.socket_props_per_material[
            context.object.active_material.name
        ].collection

        # define UI fields for every socket property
        # NOTE: if I don't sort the input nodes, everytime one of the nodes is
        # selected in the graph it moves to the bottom of the panel (?).
        # TODO: sort by date of creation? ---I didn't find an easy way to do it
        layout = self.layout
        for i_n, nd in enumerate(
            sorted(list_input_nodes, key=lambda x: x.name)
        ):
            row = layout.row()

            # if first node: add labels for
            # name, min, max and randomisation toggle
            if i_n == 0:
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                # input node name
                col1.label(text=nd.name)
                col1.alignment = "CENTER"

                # min label
                col3.alignment = "CENTER"
                col3.label(text="min")

                # max label
                col4.alignment = "CENTER"
                col4.label(text="max")

            # if not first node: add just node name
            else:
                row.separator(factor=1.0)  # add empty row before each node
                row = layout.row()
                row.label(text=nd.name)

            # add sockets for this node in the subseq rows
            for sckt in nd.outputs:
                # split row in 5 columns
                row = layout.row()
                row_split = row.split()
                col1 = row_split.column(align=True)
                col2 = row_split.column(align=True)
                col3 = row_split.column(align=True)
                col4 = row_split.column(align=True)
                col5 = row_split.column(align=True)

                # socket name
                col1.alignment = "RIGHT"
                col1.label(text=sckt.name)

                # socket current value
                col2.prop(
                    sckt,
                    "default_value",
                    icon_only=True,
                )
                col2.enabled = False  # current value is not editable

                # socket min and max columns
                socket_id = nd.name + "_" + sckt.name
                for m_str, col in zip(["min", "max"], [col3, col4]):
                    # if socket is a color: format min/max as a color picker
                    # and an array (color picker doesn't include alpha value)
                    if type(sckt) == bpy.types.NodeSocketColor:
                        # color picker
                        col.template_color_picker(
                            sockets_props_collection[socket_id],
                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                        )
                        # array
                        for j, cl in enumerate(["R", "G", "B", "alpha"]):
                            col.prop(
                                sockets_props_collection[socket_id],
                                m_str
                                + "_"
                                + cs.socket_type_to_attr[type(sckt)],
                                icon_only=False,
                                text=cl,
                                index=j,
                            )
                    # if socket is not color type: format as a regular property
                    else:
                        col.prop(
                            sockets_props_collection[socket_id],
                            m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                            icon_only=True,
                        )

                # randomisation toggle
                col5.prop(
                    sockets_props_collection[socket_id],
                    "bool_randomise",
                    icon_only=True,
                )

        # # add randomise button for operator
        # row = layout.row(align=True)
        # row_split = row.split()
        # col1 = row_split.column(align=True)
        # col2 = row_split.column(align=True)
        # col3 = row_split.column(align=True)
        # col4 = row_split.column(align=True)
        # col5 = row_split.column(align=True)
        # col5.operator("node.randomise_socket", text="Randomise")


# ------------------------------------
classes = [SocketProperties, ColSocketProperties, SamplePanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

        if cls == ColSocketProperties:
            bp = bpy.props
            bpy.types.Scene.socket_props_per_material = bp.CollectionProperty(
                type=ColSocketProperties
            )

    for attr, attr_val in zip(
        ["socket_type_to_attr", "socket_type_to_ini_min_max"],
        [MAP_SOCKET_TYPE_TO_ATTR, MAP_SOCKET_TYPE_TO_INI_MIN_MAX],
    ):
        setattr(bpy.types.Scene, attr, attr_val)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    list_attr = [
        "socket_props_per_material",
        "socket_type_to_attr",
        "socket_type_to_ini_min_max"
        #        "candidate_sockets",
    ]
    for attr in list_attr:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)


if __name__ == "__main__":
    register()
