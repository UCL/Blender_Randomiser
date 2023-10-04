import bpy

from ..property_classes.collection_UD_socket_properties import SocketProperties
from ..ui import attr_get_type, get_attr_only_str, get_obj_str


# ---------------------------------------------------
# Collection of Geometry Node groups (GNGs)
# ---------------------------------------------------
def compute_UD_props_sets(self):
    """Compute the relevant sets of geometry node groups (GNGs) and
    add them to self.

    These sets include:
    - the set of GNGs already in the collection
    - the set of GNGs in the Blender scene / data structure
    - the set of GNGs that are only in one of the two previous sets

    """
    # set of GNGs already in collection
    self.set_UD_props_in_collection = set(UD.name for UD in self.collection)

    # for UD in self.collection:
    ##print("self.collection !!!!!!!!!! ", UD.name)

    # set of node groups in Blender data structure
    self.set_UD_props_in_data = set(UD.name for UD in self.candidate_UD_props)

    # for UD in self.candidate_UD_props:
    ## print("self.candidate_UD_props !!!!!!!!!! ", UD.name)

    # pdb.set_trace()

    ### REMOVE????
    # set of node groups in one of the sets only
    self.set_UD_props_in_one_only = (
        self.set_UD_props_in_collection.symmetric_difference(
            self.set_UD_props_in_data
        )
    )


def get_update_UD_props_collection(self):
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
    compute_UD_props_sets(self)

    # if there are node groups that exist only in the Blender
    # data structure, or only in the collection: edit the collection
    if self.set_UD_props_in_one_only:
        set_update_UD_props_collection(self, True)
        return True
    else:
        return False


def set_update_UD_props_collection(self, value):
    """Setter function for the 'update_gngs_collection'
    attribute

    Parameters
    ----------
    value : _type_
        _description_
    """

    ##### ISSUE WITH DUPLICATION?????
    # if update value is True
    if value:
        # if the update fn is triggered directly and not via
        # the getter function: compute the required sets here
        if not hasattr(self, "set_UD_props_in_one_only"):
            compute_UD_props_sets(self)

        # for all node groups that are in one set only
        for UD_name in self.set_UD_props_in_one_only:
            # if only in collection: remove it from the collection

            if UD_name in self.set_UD_props_in_collection:
                self.collection.remove(self.collection.find(UD_name))

            # if only in Blender data structure: add it to the collection
            if UD_name in self.set_UD_props_in_data:
                UD = self.collection.add()
                UD.name = UD_name

        # TODO: do we need to sort collection of node groups?
        # (otherwise their order is not guaranteed, this is relevant for
        #  indexing node groups via subpanel indices)
        # it is not clear how to sort collection of properties...
        # https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner


class ColUDParentProps(bpy.types.PropertyGroup):
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

    # # collection of [collections of socket properties] (one per node group)
    # collection: bpy.props.CollectionProperty(  # type: ignore
    #     type=ColUDSocketProperties  # elements in the collection
    # )

    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )
    # autopopulate collection of geometry node groups
    update_UD_props_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_UD_props_collection,
        set=set_update_UD_props_collection,
    )

    ##### CHECK IF VALUE IS PROPERTY HERE FIRST
    # - make sure working for correct string first

    # candidate geometry node groups
    @property
    def candidate_UD_props(self):  # getter method
        """Return list of geometry node groups
        with nodes that start with the random keyword inside them

        Returns
        -------
        _type_
            _description_
        """

        # get_attr_only_strbpy.context.scene.custom
        # self is the collection of node groups
        list_UD_props = []
        objects_in_scene = []
        for i, key in enumerate(bpy.data.objects):
            # print(i)
            # print(key.name)
            objects_in_scene.append(key.name)
        for UD in bpy.context.scene.custom:
            if "[" in UD.name:
                # print("ERROR ======= UD.name", UD.name)
                # print("ERROR ======== attr_str", get_attr_only_str(UD.name))
                obj_str = get_obj_str(UD.name)
                # print(obj_str)

                for i, obj in enumerate(objects_in_scene):
                    #        regex=re.compile(r'^test-\d+$')

                    if obj in obj_str:
                        # print("Yay found cube")
                        idx = i

                # if (
                #     attr_get_type(
                #         bpy.data.objects["Cube"], get_attr_only_str(UD.name)
                #     )[1]
                #     != "dummy"
                # ):

                if (
                    attr_get_type(
                        bpy.data.objects[idx], get_attr_only_str(UD.name)
                    )[1]
                    != "dummy"
                ):
                    list_UD_props.append(UD)
            elif (
                attr_get_type(bpy.context.scene, get_attr_only_str(UD.name))[1]
                != "dummy"
            ):
                list_UD_props.append(UD)

        # list_UD_props = [
        #     UD
        #     for UD in bpy.context.scene.custom
        #     if (
        #         attr_get_type(bpy.context.scene,
        # get_attr_only_str(UD.name))[1]
        #         != "dummy"
        #     )
        #     # != "dummy"
        #     # if attr_get_type(bpy.context.scene,UD)[2] != 'dummy'
        #     # nd
        #     # for nd in bpy.data.node_groups
        #     # if nd.type == "GEOMETRY"
        #     # and (
        #     #     any(
        #     #         [
        #     #             ni.name.lower().startswith(
        #     #                 config.DEFAULT_RANDOM_KEYWORD
        #     #             )
        #     #             for ni in nd.nodes
        #     #         ]
        #     #     )
        #     # )
        # ]
        # print("type list_UD_props ========== ", type(list_UD_props[0]))
        # # sort by name
        # list_node_groups = sorted(
        #     list_materials,
        #     key=lambda mat: mat.name.lower()
        # )
        # print(list_UD_props)
        return list_UD_props


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColUDParentProps)

    # make the property available via bpy.context.scene...
    # (i.e., bpy.context.scene.socket_props_per_gng)
    bpy.types.Scene.socket_props_per_UD = bpy.props.PointerProperty(
        type=ColUDParentProps
    )


def unregister():
    bpy.utils.unregister_class(ColUDParentProps)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_UD"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)
