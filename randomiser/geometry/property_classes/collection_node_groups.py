import bpy

from .collection_geom_socket_properties import ColGeomSocketProperties


# ---------------------------------------------------
# Collection of Geometry Node groups (ColMaterials)
# ---------------------------------------------------
def compute_node_groups_sets(self):
    # set of node groups already in collection
    self.set_node_groups_in_collection = set(gr.name for gr in self.collection)

    # set of node groups in Blender data structure
    self.set_node_groups_in_data = set(
        gr.name for gr in self.candidate_geom_node_groups
    )

    # set of node groups in one only
    self.set_node_groups_in_one_only = (
        self.set_node_groups_in_collection.symmetric_difference(
            self.set_node_groups_in_data
        )
    )


def get_update_node_groups_collection(self):
    compute_node_groups_sets(self)

    # if there are node groups in one set only
    if self.set_node_groups_in_one_only:
        set_update_node_groups_collection(self, True)
        return True
    else:
        return False


def set_update_node_groups_collection(self, value):
    # if update value is True
    if value:
        # if the update fn is triggered directly and not via
        # getter fn: compute sets
        if not hasattr(self, "set_node_groups_in_one_only"):
            compute_node_groups_sets(self)

        # for all node groups that are in one only
        for gr_name in self.set_node_groups_in_one_only:
            # if only in collection: remove
            if gr_name in self.set_node_groups_in_collection:
                self.collection.remove(self.collection.find(gr_name))

            # if only in data structure: add to collection
            if gr_name in self.set_node_groups_in_data:
                gr = self.collection.add()
                gr.name = gr_name

        # TODO: do we need to sort collection of node groups?
        # (otherwise their order is not guaranteed, this is relevant for
        #  indexing node groups via subpanel indices)
        # it is not clear how to sort collection of properties...
        # https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner
        # self.collection = sorted(
        #     self.collection,
        #     key=lambda mat: mat.name.lower()
        # )


class ColGeomNodeGroups(bpy.types.PropertyGroup):
    # collection of [collections of socket properties] (one per node group)
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=ColGeomSocketProperties
    )

    # autopopulate collection of geometry node groups
    update_geom_node_groups_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_node_groups_collection,
        set=set_update_node_groups_collection,
    )

    # candidate geometry node groups
    @property
    def candidate_geom_node_groups(self):  # getter method
        # self is the collection of node groups
        list_node_groups = [
            nd for nd in bpy.data.node_groups if nd.type == "GEOMETRY"
        ]
        return list_node_groups


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------


def register():
    bpy.utils.register_class(ColGeomNodeGroups)

    # make available via bpy.context.scene...
    bprop = bpy.props
    bpy.types.Scene.socket_props_per_geom_nodegroup = bprop.PointerProperty(
        type=ColGeomNodeGroups
    )


def unregister():
    bpy.utils.unregister_class(ColGeomNodeGroups)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_geom_nodegroup"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)
