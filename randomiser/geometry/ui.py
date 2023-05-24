import bpy

# from .. import utils
# from . import config
from ..material.ui import TemplatePanel


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomGeometryNodes(TemplatePanel):
    bl_idname = "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise GEOMETRY"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        column = self.layout.column(align=True)
        column.label(
            text=(
                "Click on a node group to display its graph"
                "on the Geometry Node Editor"
            )
        )


# ------------------------------
# Subpanel for each node group
# -----------------------------
# class SubPanelRandomGeometryNodes(TemplatePanel):
#     @classmethod
#     def poll():
#         pass

#     def draw_header(self, context: Context):
#         return super().draw_header(context)

#     def draw(self, context: Context):
#         return super().draw(context)


# -----------------------
# Classes to register
# ---------------------

# Main panel
list_classes_to_register = [
    MainPanelRandomGeometryNodes,
]

# Subpanel for each node group


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
