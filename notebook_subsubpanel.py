"""
Example to show a sub-subpanel per material

Based on this great SO answer:
https://blender.stackexchange.com/questions/185693/how-can-i-control-the-number-of-sub-panel-instances-from-an-intproperty

We register all subpanels but show them only if the poll condition is met

Downside: we do need to define a max number of subpanels
The alternative would be to define and register classes on the fly
but apparently that is less robust

"""


import bpy

MAX_NUMBER_OF_PANELS = 2


# ----------------------
# Materials count prop
# ---------------------
def get_candidate_materials(self):  # getter method
    list_materials = [mat for mat in bpy.data.materials if mat.node_tree]
    return len(list_materials)


def set_candidate_materials(self, value):
    print("The materials count property is read-only")
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
        row = layout.row()
        row.prop(
            context.scene, "materials_count"
        )  # I think this needs to be a bpy.prop


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
        return cls.subpanel_count <= context.scene.materials_count

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="BLA")


# ----------------------
# Sub-subpanel
# ---------------------
class EXAMPLE_PT_subsubpanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Example Tab"
    bl_idname = "EXAMPLE_PT_sub_sub_panel"  # what is this for?
    bl_parent_id = "EXAMPLE_PT_sub_panel"
    bl_label = ""  # this is the subpanel title but will be overwritten
    bl_options = {"DEFAULT_CLOSED"}
    # bl_context = "objectmode"  # what is this for?

    @classmethod
    def poll(cls, context):
        # only display subpanels for which this is true
        return cls.subsubpanel_count <= 2  # context.scene.materials_count

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="subBLA")


# ----------------------
# List classes to register
# ---------------------
list_clasess = [
    EXAMPLE_PT_panel,  # do not register subpanel!
]

# we register each subpanel individually (all MAX_NUMBER_OF_PANELS)
for i in range(MAX_NUMBER_OF_PANELS):
    panel = type(
        f"EXAMPLE_PT_subpanel_{i}",
        (
            EXAMPLE_PT_subpanel,
            bpy.types.Panel,
        ),
        {
            "bl_idname": f"EXAMPLE_PT_sub_panel_{i}",
            "bl_label": f"Material {i}",
            "subpanel_count": i + 1,
        },
    )
    list_clasess.append(panel)  # type: ignore

    for k in range(MAX_NUMBER_OF_PANELS):
        subsubpanel = type(
            f"EXAMPLE_PT_subsubpanel_{i}_{k}",
            (
                EXAMPLE_PT_subsubpanel,  # panel
                bpy.types.Panel,
            ),
            {
                "bl_idname": f"EXAMPLE_PT_sub_sub_panel_{i}_{k}",
                "bl_parent_id": f"EXAMPLE_PT_sub_panel_{i}",  # ---- added
                "bl_label": f"Node group {k}",
                "subsubpanel_count": k,
            },
        )
        list_clasess.append(subsubpanel)  # type: ignore


# ----------------------
# Register / unregister functions
# ---------------------
def register():
    for cls in list_clasess:
        bpy.utils.register_class(cls)

    bpy.types.Scene.materials_count = bpy.props.IntProperty(
        name="Materials count",
        default=1,
        get=get_candidate_materials,
        set=set_candidate_materials,
    )

    print("registered")


def unregister():
    for cls in list_clasess:
        bpy.utils.unregister_class(cls)

    # remove from bpy.context.scene...
    if hasattr(bpy.types.Scene, "materials_count"):
        delattr(bpy.types.Scene, "materials_count")

    print("unregistered")


if __name__ == "__main__":
    register()
