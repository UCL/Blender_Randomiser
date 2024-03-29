import bpy

from ..property_classes.collection_UD_socket_properties import SocketProperties
from ..ui import attr_get_type, get_attr_only_str, get_obj_str


# ---------------------------------------------------
# Collection of UD props
# ---------------------------------------------------
def compute_UD_props_sets(self):
    """Compute the relevant sets of UD props and
    add them to self.

    These sets include:
    - the set of UD props already in the collection
    - the set of UD props in the Blender scene / data structure
    - the set of UD props that are only in one of the two previous sets

    """
    # set of UD props already in collection
    self.set_UD_props_in_collection = set(UD.name for UD in self.collection)

    # set of UD props in Blender data structure
    self.set_UD_props_in_data = set(UD.name for UD in self.candidate_UD_props)

    # set of UD props in one of the sets only
    self.set_UD_props_in_one_only = (
        self.set_UD_props_in_collection.symmetric_difference(
            self.set_UD_props_in_data
        )
    )


def get_update_UD_props_collection(self):
    """Getter function for the 'update_UD_props_collection'
    attribute.

    Checks if the collection of UD props needs
    to be updated, and updates it if required.

    The collection will need to be updated if there
    are UD props that have been added/deleted from the scene.

    Returns
    -------
    boolean
        returns True if the collection is updated,
        otherwise it returns False
    """
    # compute relevant UD props sets and add them to self
    compute_UD_props_sets(self)

    # if there are UD props that exist only in the Blender
    # data structure, or only in the collection: edit the collection
    if self.set_UD_props_in_one_only:
        set_update_UD_props_collection(self, True)
        return True
    else:
        return False


def set_update_UD_props_collection(self, value):
    """Setter function for the 'update_UD_props_collection'
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
        if not hasattr(self, "set_UD_props_in_one_only"):
            compute_UD_props_sets(self)

        # for all UD props that are in one set only
        for UD_name in self.set_UD_props_in_one_only:
            # if only in collection: remove it from the collection

            if UD_name in self.set_UD_props_in_collection:
                self.collection.remove(self.collection.find(UD_name))

            # if only in Blender data structure: add it to the collection
            if UD_name in self.set_UD_props_in_data:
                UD = self.collection.add()
                UD.name = UD_name


class ColUDParentProps(bpy.types.PropertyGroup):
    """Collection of UD props

    This class has two attributes and one property
    - collection (attribute): holds the collection of UD props
    - update_UD_props_collection (attribute): helper attribute
      to force updates on
      the collection of UD props
    - candidate_UD_props (property): returns the updated list of UD props
    defined in the scene

    This data will be made availabe via bpy.context.scene.socket_props_per_UD

    Parameters
    ----------
    bpy : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    # # collection of user defined properties
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=SocketProperties
    )
    # autopopulate collection of user defined properties
    update_UD_props_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_UD_props_collection,
        set=set_update_UD_props_collection,
    )

    # candidate UD props
    @property
    def candidate_UD_props(self):  # getter method
        """Return list of UD props from UIlist

        Returns
        -------
        _type_
            _description_
        """

        # get_attr_only_strbpy.context.scene.custom
        # self is the collection of UD props
        list_UD_props = []

        objects_in_scene = []
        for i, key in enumerate(bpy.data.objects):
            objects_in_scene.append(key.name)

        for UD in bpy.context.scene.custom:
            if "[" in UD.name:
                obj_str = get_obj_str(UD.name)

                for i, obj in enumerate(objects_in_scene):
                    if obj in obj_str:
                        current_obj = obj
                        idx = i

                if "Camera" in current_obj:
                    if (
                        attr_get_type(
                            bpy.data.cameras[idx], get_attr_only_str(UD.name)
                        )[1]
                        != "dummy"
                    ):
                        list_UD_props.append(UD)

                else:
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

        return list_UD_props


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    bpy.utils.register_class(ColUDParentProps)

    # make the property available via bpy.context.scene...
    bpy.types.Scene.socket_props_per_UD = bpy.props.PointerProperty(
        type=ColUDParentProps
    )


def unregister():
    bpy.utils.unregister_class(ColUDParentProps)

    # remove from bpy.context.scene...
    attr_to_remove = "socket_props_per_UD"
    if hasattr(bpy.types.Scene, attr_to_remove):
        delattr(bpy.types.Scene, attr_to_remove)
