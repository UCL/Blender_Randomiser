from . import material
from . import transform


bl_info = {
    "name": "Randomisations panel",
    "blender": (
        3,
        4,
        1,
    ),  # min required version; get from running bpy.app.version
    "category": "Object",
    # optional
    "version": (1, 0, 0),
    "author": "Sofia Miñano",
    "description": ("Randomise selected parameters" "of a subset of objects"),
}


def register():
    transform.register()
    #material.register()
    # geometry.register()


def unregister():
    transform.unregister()
    #material.unregister()
    # geometry.unregister()


if __name__ == "__main__":
    register()
