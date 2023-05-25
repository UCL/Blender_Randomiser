from . import material, transform, seed, user_defined, custom_props

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
    # material.register()
    custom_props.register()
    # user_defined.register()
    # geometry.register()


def unregister():
    seed.unregister()
    # transform.unregister()
    # material.unregister()
    custom_props.unregister()
    # user_defined.unregister()
    # geometry.unregister()


if __name__ == "__main__":
    register()
