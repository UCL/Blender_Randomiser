"""
MWE 1
Based on example described at
https://blender.stackexchange.com/questions/141179/how-to-populate-uilist-with-all-material-slot-in-scene-2-8/141207#141207

The idea is that we define a Blender bool prop linked to bpy.context.scene
with custom get and set fns. When we get its value, it checks if the collection
of sockets property needs an update (because new nodes have been added to the
graph) and if so it updates it.

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
    """
    Properties for a socket element

    Types of properties:---these relate to UI buttons
     bpy.props.
              BoolProperty(
              BoolVectorProperty(
              CollectionProperty(
              EnumProperty(
              FloatProperty(
              FloatVectorProperty(
              IntProperty(
              IntVectorProperty(
              PointerProperty(
              RemoveProperty(
              StringProperty(

    """

    # name (we can use it to access sockets in collection by name)
    name: bpy.props.StringProperty()  # type: ignore

    min_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore
    max_float_1d: bpy.props.FloatVectorProperty(size=1)  # type: ignore

    ### bool
    bool_randomise: bpy.props.BoolProperty()  # type: ignore


# --------------------------------------
def get_candidate_sockets(self):  # get_scene_materials
    # list input nodes (eventually, for all materials?)
    list_input_nodes = [
        nd
        for nd in bpy.data.materials["Material"].node_tree.nodes
        if len(nd.inputs) == 0 and nd.name.lower().startswith("random".lower())
    ]
    # list of sockets (eventually if linked)
    list_of_sockets = [out for nd in list_input_nodes for out in nd.outputs]
    return list_of_sockets


# ------------------------------------
def get_update_collection(self):
    # Get fn for update_collection' property
    # It will run when the property value is 'get' and
    # it will update the *collection of socket properties* if required

    # set of sockets in collection
    set_of_sockets_in_collection_of_props = set(
        sck_p.name for sck_p in self.sockets2randomise_props
    )

    # set of sockets in graph
    set_of_sockets_in_graph = set(
        sck.node.name + "_" + sck.name for sck in self.candidate_sockets
    )
    collection_needs_update = (
        set_of_sockets_in_collection_of_props.symmetric_difference(
            set_of_sockets_in_graph
        )
    )

    # if there is a diff: overwrite the collection of sockets
    # returns True if it was overwritten
    if collection_needs_update:
        set_update_collection(self, True)
        return True  # ?
    else:
        return False

    # originally: return False # why?


def set_update_collection(self, value):
    # Set fn for the update_collection scene property
    # It will run when the property value is 'set'
    # It will overwrite the collection of socket properties
    if value:
        self.sockets2randomise_props.clear()  # ---ideally just update!
        for sckt in self.candidate_sockets:
            sckt_prop = self.sockets2randomise_props.add()
            sckt_prop.name = sckt.node.name + "_" + sckt.name
            sckt_prop.bool_randomise = True
            sckt_prop.min_float_1d = (0.0,)
            sckt_prop.max_float_1d = (100.0,)
        # return True


# --------------------------------------
classes = [SocketProperties]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

        if cls == SocketProperties:
            bp = bpy.props
            bpy.types.Scene.sockets2randomise_props = bp.CollectionProperty(
                type=SocketProperties  # type of the elements in the collection
            )

    bpy.types.Scene.candidate_sockets = property(
        fget=get_candidate_sockets
    )  # fget
    # bpy.context.scene.candidate_sockets will provide an updated list of
    # candidate sockets
    # What is a managed property?

    bpy.types.Scene.update_collection_socket_props = bpy.props.BoolProperty(
        get=get_update_collection,  # get_update_materials;
        # this fn is called when
        # bpy.context.scene.update_collection_socket_props
        set=set_update_collection,  # set_update_materials;
        # this fn is called when
        # bpy.context.scene.update_collection_socket_props = 'patata'
        name="Update collection of socket properties",
    )
    # if I 'get' this property: it will update if required
    #   > bpy.context.scene.update_collection_socket_props
    # if I set this property to True: it will force an update
    #   >  bpy.context.scene.update_collection_socket_props = True

    # I think I can use this:
    # - before drawing panel
    # - to initialise properties (instead of handlers)

    # bpy.types.Scene.active_material_index = IntProperty()
    # bpy.types.Scene.material_slots = CollectionProperty(
    #     type=SceneMaterialSlot)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.active_material_index
    # del bpy.types.Scene.material_slots


if __name__ == "__main__":
    register()
