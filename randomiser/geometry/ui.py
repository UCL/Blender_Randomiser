import bpy

# from .. import utils
# from . import config


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomGeometryNodes(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"  # this shows up as the tab name

    bl_idname = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise GEOMETRY"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        self.layout.label(text="Hello World")
        # pass
        # column = self.layout.column(align=True)
        # column.label(text="Select material to see available sockets.")


# -----------------------
# Classes to register
# ---------------------

# Main panel
list_classes_to_register = [
    MainPanelRandomGeometryNodes,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("geometry UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("geometry UI unregistered")
