from . import material, transform, geometry, seed, define_prop  # random_all

bl_info = {
    "name": "Randomisations panel",
    "blender": (
        3,
        4,
        1,
    ),  # min required version; get from running bpy.app.version
    "category": "Object",
    # optional
    "version": (0, 1, 0),
    "author": "Sofía Miñano and Ruaridh Gollifer",
    "description": ("Randomise selected parameters" "of a subset of objects"),
}


def register():
    seed.register()
    # transform.register()
    material.register()
    geometry.register()
    define_prop.register()
    # random_all.register()


def unregister():
    seed.unregister()
    # transform.unregister()
    material.unregister()
    geometry.unregister()
    define_prop.unregister()
    # random_all.unregister()


if __name__ == "__main__":
    register()
