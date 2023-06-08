import bpy

from ... import config
from .collection_geom_socket_properties import ColGeomSocketProperties


# ---------------------------------------------------
# Collection of Geometry Node groups (GNGs)
# ---------------------------------------------------
def compute_node_groups_sets(self):
    """Compute the relevant sets of geometry node groups (GNGs) and
    add them to self.

    These sets include:
    - the set of GNGs already in the collection
    - the set of GNGs in the Blender scene / data structure
    - the set of GNGs that are only in one of the two previous sets

    """
    # set of GNGs already in collection
    self.set_node_groups_in_collection = set(gr.name for gr in self.collection)

    # set of node groups in Blender data structure
    self.set_node_groups_in_data = set(gr.name for gr in self.candidate_gngs)

    # set of node groups in one of the sets only
    self.set_node_groups_in_one_only = (
        self.set_node_groups_in_collection.symmetric_difference(
            self.set_node_groups_in_data
        )
    )


def get_update_node_groups_collection(self):
    """Getter function for the 'update_gngs_collection'
    attribute.

    Checks if the collection of GNGs needs
    to be updated, and updates it if required.

    The collection will need to be updated if there
    are GNGs that have been added/deleted from the scene.

    Returns
    -------
    boolean
        returns True if the collection is updated,
        otherwise it returns False
    """
    # compute relevant GNG sets and add them to self
    compute_node_groups_sets(self)

    # if there are node groups that exist only in the Blender
    # data structure, or only in the collection: edit the collection
    if self.set_node_groups_in_one_only:
        set_update_node_groups_collection(self, True)
        return True
    else:
        return False


def set_update_node_groups_collection(self, value):
    """Setter function for the 'update_gngs_collection'
    attribute

    Parameters
    ----------
    value : _type_
        _description_
    """

    # if update value is True
    if value:
        # if the update fn is triggered directly and not via
        # the getter function: compute the required sets here
        if not hasattr(self, "set_node_groups_in_one_only"):
            compute_node_groups_sets(self)

        # for all node groups that are in one set only
        for gr_name in self.set_node_groups_in_one_only:
            # if only in collection: remove it from the collection
            if gr_name in self.set_node_groups_in_collection:
                self.collection.remove(self.collection.find(gr_name))

            # if only in Blender data structure: add it to the collection
            if gr_name in self.set_node_groups_in_data:
                gr = self.collection.add()
                gr.name = gr_name

        # TODO: do we need to sort collection of node groups?
        # (otherwise their order is not guaranteed, this is relevant for
        #  indexing node groups via subpanel indices)
        # it is not clear how to sort collection of properties...
        # https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner


class ColGeomNodeGroups(bpy.types.PropertyGroup):
    """Collection of Geometry Node Groups

    This class has two attributes and one property
    - collection (attribute): holds the collection of GNGs
    - update_gngs_collection (attribute): helper attribute to force updates on
      the collection of GNGs
    - candidate_gngs (property): returns the updated list of geometry node
      groups defined in the scene

    This data will be made availabe via bpy.context.scene.socket_props_per_gng

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # collection of [collections of socket properties] (one per node group)
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=ColGeomSocketProperties  # elements in the collection
    )

    # autopopulate collection of geometry node groups
    update_gngs_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_node_groups_collection,
        set=set_update_node_groups_collection,
    )

    # candidate geometry node groups
    @property
    def candidate_gngs(self):  # getter method
        """Return list of geometry node groups
        with nodes that start with the random keyword inside them

        Returns
        -------
        _type_
            _description_
        """
        # self is the collection of node groups
        list_node_groups = [
            nd
            for nd in bpy.data.node_groups
            if nd.type == "GEOMETRY"
            and (
                any(
                    [
                        ni.name.lower().startswith(
                            config.DEFAULT_RANDOM_KEYWORD
                        )
                        for ni in nd.nodes
                    ]
                )
            )
        ]
        # # sort by name
        # list_node_groups = sorted(
        #     list_materials,
        #     key=lambda mat: mat.name.lower()
        # )
        return list_node_groups


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColGeomNodeGroups)

    # make the property available via bpy.context.scene...
    # (i.e., bpy.context.scene.socket_props_per_gng)
    bpy.types.Scene.socket_props_per_gng = bpy.props.PointerProperty(
        type=ColGeomNodeGroups
    )


def unregister():
    bpy.utils.unregister_class(ColGeomNodeGroups)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_UD_property"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)
