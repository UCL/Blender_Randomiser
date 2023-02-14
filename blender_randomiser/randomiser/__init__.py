### Imports
# for reference check:
# /Applications/Blender.app/Contents/Resources/3.4/scripts/addons/object_scatter

from . import geometry, material, transforms

bl_info = {
    "name": "Add randomisations",
    "blender": (
        3,
        4,
        1,
    ),  # min required version; get from running bpy.app.version
    "category": "Object",
    # optional
    "version": (1, 0, 0),
    "author": "Sofia Miñano",
    "description": ("Randomise selected parameters" "of the active object"),
}


def register():
    transforms.register()
    geometry.register()
    material.register()


def unregister():
    transforms.unregister()
    geometry.unregister()
    material.register()


if __name__ == "__main__":
    register()
