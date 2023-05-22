import bpy


# -------
# Panel
# -------
class PanelRandomSeed(bpy.types.Panel):
    """Class defining the panel for the
    randomisation seed

    """

    bl_idname = "SEED_PT_random_seed_global"
    bl_label = "Random SEED"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        # Seed
        row = self.layout.row(align=True)
        split = row.split()
        left_col = split.column(align=True)
        right_col = split.column(align=True)

        # put the toggle on the left col
        left_col_row = left_col.row(align=True)
        left_col_row.alignment = "RIGHT"  # alignment first!
        left_col_row.prop(
            context.scene.seed_properties, "seed_toggle", icon_only=True
        )
        left_col_row.label(text="Set random seed")

        # put field in right col
        right_col.enabled = (
            context.scene.seed_properties.seed_toggle
        )  # only disable the next part of the row
        right_col.prop(context.scene.seed_properties, "seed", icon_only=True)


# -----------------------
# Classes to register
# -----------------------
list_classes_to_register = [
    PanelRandomSeed,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("seed UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("seed UI unregistered")
