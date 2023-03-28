"""
MWE 2
Based on example described at
https://blender.stackexchange.com/questions/211247/cant-find-update-callback-for-collectionproperty

A more concise alternative to the MWE, in which the aux boolean property is
defined as an attribute of a blender property with two attributes:
the collection of sockets and this boolean aux property.

"""

import bpy

bl_info = {
    "name": "Selected Materials",
    "author": "batFINGER, (edited by Iraki Kupunia)",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "View3D > UI > Item",
    "description": "List selected Materials",
    "warning": "",
    "doc_url": "https://blender.stackexchange.com/a/141207/15543",
    "category": "Materials",
}


class SocketProperties(bpy.types.PropertyGroup):
    # name (we can use it to access sockets in collection by name)
    name: bpy.props.StringProperty()  # type: ignore

    min_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore
    max_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore

    ### bool
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


def get_update_collection(self):
    # Get fn for update_collection' property
    # It will run when the property value is 'get' and
    # it will update the *collection of socket properties* if required

    # set of sockets in collection
    set_of_sockets_in_collection_of_props = set(
        sck_p.name for sck_p in self.collection
    )

    # set of sockets in graph
    set_of_sockets_in_graph = set(
        sck.node.name + "_" + sck.name
        for sck in bpy.context.scene.candidate_sockets
    )
    collection_needs_update = (
        set_of_sockets_in_collection_of_props.symmetric_difference(
            set_of_sockets_in_graph
        )
    )

    # if there is a diff: overwrite the collection of sockets
    if collection_needs_update:
        set_update_collection(self, True)
        return True  # if returns True, it has been updated
    else:
        return False  # if returns False, it hasnt


def set_update_collection(self, value):
    # Set fn for the update_collection scene property
    # It will run when the property value is 'set'
    # It will overwrite the collection of socket properties
    if value:
        self.collection.clear()
        # ideally just update rather than clear(), but
        # All properties define update functions except for CollectionProperty
        # https://docs.blender.org/api/current/bpy.props.html#update-example
        for sckt in bpy.context.scene.candidate_sockets:
            sckt_prop = self.collection.add()
            sckt_prop.name = sckt.node.name + "_" + sckt.name
            sckt_prop.bool_randomise = True


class ColSocketProperties(bpy.types.PropertyGroup):
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )

    # 'dummy' attribute to update collection
    update_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,  # initial value
        get=get_update_collection,
        # this fn is called when
        # bpy.context.scene.update_collection_socket_props
        set=set_update_collection,
        # this fn is called when
        # bpy.context.scene.sockets2_randomise_props.update_collection = True
    )


def get_candidate_sockets(self):
    # list input nodes
    list_input_nodes = [
        nd
        for nd in bpy.data.materials["Material"].node_tree.nodes
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random".lower())
    ]
    # list of sockets (eventually if linked?)
    list_sockets = [out for nd in list_input_nodes for out in nd.outputs]
    return list_sockets


# --------------------------------------
classes = [SocketProperties, ColSocketProperties]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

        if cls == ColSocketProperties:
            bp = bpy.props
            bpy.types.Scene.sockets2randomise_props = bp.PointerProperty(
                type=ColSocketProperties
            )

    bpy.types.Scene.candidate_sockets = property(fget=get_candidate_sockets)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.candidate_sockets
    # del bpy.types.Scene.material_slots


if __name__ == "__main__":
    register()
