import bpy


# -------
# Panel
# -------
class PanelRandomAll(bpy.types.Panel):
    """Class defining the panel for the
    randomise all and save parameter button

    """

    bl_idname = "RAND_ALL_PT_random_all"
    bl_label = "Random RAND_ALL"
    # title of the panel / label displayed to the user
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Randomiser"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        # Random all
        layout = self.layout

        # Create a simple row.
        # Create an row where the buttons are aligned to each other.
        row = layout.row()
        row_split = row.split()
        col1 = row_split.column(align=True)
        # col2 = row_split.column(align=True)
        # col3 = row_split.column(align=True)
        # col4 = row_split.column(align=True)
        # col5 = row_split.column(align=True)

        col1.label(text=" Randomise all:")
        # col2.label(text="")
        # col3.label(text="min")
        # col4.label(text="max")
        # col5.label(text="")

        ###################
        # Camera positon
        # row = layout.row()  # row = layout.row(align=True)
        # row.label(text="x")

        # row_split = row.split()
        # col1 = row_split.column(align=True)
        # col2 = row_split.column(align=True)
        # col3 = row_split.column(align=True)
        # col4 = row_split.column(align=True)

        # Randomise button
        col = self.layout.column()
        col.operator("camera.randomise_all", text="Randomise")

        # Camera rotation y
        row = layout.row()
        row.label(text="Save randomisation outputs")
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)

        col1.operator("camera.save_param_out", text="Save Parameter Outputs")
        # col1.enabled = False
        col2.prop(
            context.scene.rand_all_properties,
            "tot_frame_no",
            icon_only=True,
        )

        # row = self.layout.row(align=True)
        # split = row.split()
        # left_col = split.column(align=True)
        # right_col = split.column(align=True)

        # # put the toggle on the left col
        # left_col_row = left_col.row(align=True)
        # left_col_row.alignment = "RIGHT"  # alignment first!
        # left_col_row.prop(
        #     context.scene.seed_properties, "seed_toggle", icon_only=True
        # )
        # left_col_row.label(text="Set random seed")

        # # put field in right col
        # right_col.enabled = (
        #     context.scene.seed_properties.seed_toggle
        # )  # only disable the next part of the row
        # right_col.prop(context.scene.seed_properties, "seed", icon_only=True)


# -----------------------
# Classes to register
# -----------------------
list_classes_to_register = [
    PanelRandomAll,
]


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)

    print("Random_all UI registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    print("Random_all UI unregistered")
