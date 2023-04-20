"""
Example to show a subpanel per material

Based on this great SO answer:
https://blender.stackexchange.com/questions/185693/how-can-i-control-the-number-of-sub-panel-instances-from-an-intproperty

We register all subpanels but show them only if the poll condition is met

Downside: we do need to define a max number of subpanels
The alternative would be to define and register classes on the fly
but apparently that is less robust

"""


import bpy

MAX_NUMBER_OF_PANELS = 100


# ----------------------
# List candidate materials prop
# ---------------------
def get_candidate_materials(self):  # getter method
    list_materials = [mat.name for mat in bpy.data.materials if mat.node_tree]
    return list_materials  # len(list_materials)


def set_candidate_materials(self, value):
    print("The list of candidate materials is read-only")
    return None


# ----------------------
# Main panel
# ---------------------
class EXAMPLE_PT_panel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Example Tab"
    bl_idname = "EXAMPLE_PT_panel"
    bl_label = "Randomise material"

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is the main panel.")


# ----------------------
# Subpanel
# ---------------------
class EXAMPLE_PT_subpanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Example Tab"
    bl_idname = "EXAMPLE_PT_sub_panel"  # what is this for?
    bl_parent_id = "EXAMPLE_PT_panel"
    bl_label = ""  # this is the subpanel title but will be overwritten
    bl_options = {"DEFAULT_CLOSED"}
    # bl_context = "objectmode"  # what is this for?

    @classmethod
    def poll(cls, context):
        # only display subpanels for which this is true
        return cls.subpanel_material_idx < len(context.scene.list_materials)

    def draw_header(self, context):
        layout = self.layout
        if self.subpanel_material_idx < len(context.scene.list_materials):
            layout.label(
                text=context.scene.list_materials[self.subpanel_material_idx]
            )
        else:
            layout.label(text="PATATA")

    def draw(self, context):
        layout = self.layout
        layout.label(text="BLA")


# ----------------------
# Register / unregister
# ---------------------
list_classes_to_register = [
    EXAMPLE_PT_panel,  # do not register subpanel!
]

# we register each subpanel individually
# (we register all MAX_NUMBER_OF_PANELS panels)
for i in range(MAX_NUMBER_OF_PANELS):
    panel = type(
        f"EXAMPLE_PT_subpanel_{i}",  # user-defined class name
        (
            EXAMPLE_PT_subpanel,
            bpy.types.Panel,
        ),  # parent classes
        {
            "bl_idname": f"EXAMPLE_PT_sub_panel_{i}",
            "bl_label": "",  # f"Material {i}",
            "subpanel_material_idx": i,
            # "draw_header": draw_header,
        },
    )
    list_classes_to_register.append(panel)  # type: ignore


def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    # add list of candidate materials as managed property
    bpy.types.Scene.list_materials = property(
        fget=get_candidate_materials, fset=set_candidate_materials
    )

    print("registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # remove from bpy.context.scene...
    if hasattr(bpy.types.Scene, "list_materials"):
        delattr(bpy.types.Scene, "list_materials")

    print("unregistered")


if __name__ == "__main__":
    register()
