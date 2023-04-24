import bpy

from .collection_socket_properties import ColSocketProperties

# -----------------------------------------------------------------
# Setter / getter methods for update_materials_collection attribute
# ----------------------------------------------------------------


def compute_materials_sets(self):
    # set of materials currently in collection
    self.set_material_names_in_collection = set(
        mat.name for mat in self.collection
    )

    # set of materials in Blender data structure
    # candidate materials: those with node_tree
    self.set_material_names_in_data = set(
        mat.name for mat in self.candidate_materials
    )

    # set of materials in one only
    self.set_material_names_in_one_only = (
        self.set_material_names_in_collection.symmetric_difference(
            self.set_material_names_in_data
        )
    )


def get_update_materials_collection(self):
    # for mat in self.candidate_materials:

    compute_materials_sets(self)

    # if there are materials in one set only
    if self.set_material_names_in_one_only:
        set_update_materials_collection(self, True)
        return True
    else:
        return False


def set_update_materials_collection(self, value):
    # if update value is set to True
    if value:
        # if the update fn is triggered directly and not via
        # getter fn: compute sets
        if not hasattr(self, "set_material_names_in_one_only"):
            compute_materials_sets(self)

        # for all materials that are in one set only
        for mat_name in self.set_material_names_in_one_only:
            # - if material is in collection only: remove from collection
            if mat_name in self.set_material_names_in_collection:
                self.collection.remove(self.collection.find(mat_name))

            # - if in data structure only: add to collection
            if mat_name in self.set_material_names_in_data:
                mat = self.collection.add()
                # attributes of mat: name, collection,
                # update_sockets_collection
                mat.name = mat_name

        # TODO: do we need to sort collection of materials?
        # (otherwise their order is not guaranteed, this is relevant for
        #  indexing materials via subpanel indices)
        # it is not clear how to sort collection of properties...
        # https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner
        # self.collection = sorted(
        #     self.collection,
        #     key=lambda mat: mat.name.lower()
        # )


# ----------------
# ColMaterials
# ----------------
class ColMaterials(bpy.types.PropertyGroup):
    # collection of [collections of socket properties] (one per material)
    collection: bpy.props.CollectionProperty(  # type: ignore
        type=ColSocketProperties
    )

    # autopopulate collection of materials
    update_materials_collection: bpy.props.BoolProperty(  # type: ignore
        default=False,
        get=get_update_materials_collection,
        set=set_update_materials_collection,
    )

    # candidate materials
    # (i.e.,materials with 'Use nodes' enabled in GUI)
    @property
    def candidate_materials(self):  # getter method
        # self is the collection of materials
        list_materials = [mat for mat in bpy.data.materials if mat.use_nodes]
        # # sort by name
        # list_materials = sorted(
        #     list_materials,
        #     key=lambda mat: mat.name.lower()
        # )
        return list_materials

    # ----------------------------


def register():
    bpy.utils.register_class(ColMaterials)

    # make available via bpy.context.scene...
    bpy.types.Scene.socket_props_per_material = bpy.props.PointerProperty(
        type=ColMaterials
    )


def unregister():
    bpy.utils.unregister_class(ColMaterials)

    # remove from bpy.context.scene...
    if hasattr(bpy.types.Scene, "socket_props_per_material"):
        delattr(bpy.types.Scene, "socket_props_per_material")
