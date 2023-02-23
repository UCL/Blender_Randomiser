### Imports
# for reference check:
# /Applications/Blender.app/Contents/Resources/3.4/scripts/addons/object_scatter

from . import geometry, material, transforms
import bpy
import importlib


importlib.reload(material)

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
    # transforms.register()
    material.register()
    # geometry.register()


def unregister():
    # transforms.unregister()
    material.unregister()
    # geometry.unregister()


if __name__ == "__main__":
    register()
