# Sub panels are created by adding a bl_parent_id referring to the parent
# panel.
# https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/UI_API#Sub_Panels
#

import bpy


class EXAMPLE_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Example Tab"
    bl_options = {"DEFAULT_CLOSED"}


# main panel
class EXAMPLE_PT_panel_1(EXAMPLE_panel, bpy.types.Panel):
    bl_idname = "EXAMPLE_PT_panel_1"
    bl_label = "Main panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is the main panel.")


# subpanel--bl_parent_id
class EXAMPLE_PT_panel_2(EXAMPLE_panel, bpy.types.Panel):
    bl_parent_id = "EXAMPLE_PT_panel_1"
    bl_label = "First subpanel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="First Sub Panel of Panel 1.")


# subpanel --bl_parent_id
class EXAMPLE_PT_panel_3(EXAMPLE_panel, bpy.types.Panel):
    bl_parent_id = "EXAMPLE_PT_panel_1"
    bl_label = "Second subpanel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Second Sub Panel of Panel 1.")


list_classes_to_register = [
    EXAMPLE_PT_panel_1,
    EXAMPLE_PT_panel_2,
    EXAMPLE_PT_panel_3,
]


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("unregistered")


if __name__ == "__main__":
    register()
