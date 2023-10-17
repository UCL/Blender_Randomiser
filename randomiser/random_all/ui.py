import bpy


# -------
# Panel
# -------
class PanelRandomAll(bpy.types.Panel):
    """Class defining the panel for the
    randomise all and save parameter button

    """

    bl_idname = "RAND_ALL_PT_random_all"
    bl_label = "Randomise All and Save Output"
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

        col1.label(text="Randomise camera transforms, materials and geometry")

        row = layout.row()
        row_split = row.split()
        col1 = row_split.column(align=True)

        col1.label(text="Save output parameters for selected number of frames")

        # Randomise button
        col = self.layout.column()
        col.operator(
            "camera.save_param_out", text="Randomise All and Save Output"
        )
        # col1.enabled = False

        row = layout.row()
        row_split = row.split()
        col1 = row_split.column(align=True)
        col2 = row_split.column(align=True)

        col1.label(text="Number of Frames: ")
        col2.prop(
            context.scene.rand_all_properties,
            "tot_frame_no",
            icon_only=True,
        )


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
