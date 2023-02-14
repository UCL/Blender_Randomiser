"""
An add-on to randomise the material parameters
of the selected objects

"""
### Imports
import bpy
import numpy as np


# ---------------------------
# Properties
class PropertiesAddRandomMaterial(
    bpy.types.PropertyGroup
):  # ---these will be added to context.scene.<custom_prop> in registration
    vol_size_prop = bpy.props.FloatProperty(
        name="Target volume size",
        default=1.0,
        soft_min=0.0,
        soft_max=10.0,
        step=50,
    )  # OJO in step: the actual value is the value set here divided by 100
    vol_size: vol_size_prop  # type: ignore

    seed_toggle_prop = bpy.props.BoolProperty(
        name="Set random seed", default=False
    )
    seed_toggle: seed_toggle_prop  # type: ignore

    seed_prop = bpy.props.IntProperty(name="Seed", default=42)
    seed: seed_prop  # type: ignore


# -------------------------------
## Operators
class AddRandomMaterial(bpy.types.Operator):  # ---check types
    # docstring shows as a tooltip for menu items and buttons.
    """Add a random cube within a predefined volume"""

    bl_idname = "object.add_random_cube"  # appended to bpy.ops.
    bl_label = "Add random cube in volume"
    bl_options = {"REGISTER", "UNDO"}

    # check if the operator can be executed/invoked
    # in the current context
    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    # ----------------------
    ## Invoke
    # runs before execute, to initialise ....?
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    # -------------------------------
    ### Execute fn
    def execute(self, context):
        # add a cube primitive and link it to the scene collection
        bpy.ops.mesh.primitive_cube_add()  # returns {'FINISHED'} if successful
        cube_object = context.object

        # get inputs
        # seed: If None, fresh unpredictable entropy will be pulled from the OS
        scene = context.scene
        seed = (
            scene.random_cube_props.seed
            if scene.random_cube_props.seed_toggle
            else None
        )
        vol_size = scene.random_cube_props.vol_size

        # set location randomly within predifined volume
        rng = np.random.default_rng(
            seed
        )  # recommended constructor for the random number class Generator
        cube_object.location = vol_size * rng.random((3,)) - 0.5 * vol_size

        return {"FINISHED"}


# -------
# Panel
class PanelAddRandomMaterial(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_random_material"
    bl_label = "Randomise MATERIAL"
    # title of the panel / label displayed to the user
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Randomisation"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        # Target volume (align text label and field)
        layout = self.layout
        row = layout.row()
        split = row.split()
        left_col = split.column(align=True)
        right_col = split.column(align=True)

        left_col.alignment = "RIGHT"
        left_col.label(text="Target volume size")
        right_col.prop(
            context.scene.random_cube_props, "vol_size", icon_only=True
        )
        # alternative: layout.prop(context.scene.random_cube_props, "vol_size")

        # Seed
        row = self.layout.row(align=True)
        split = row.split()
        left_col = split.column(align=True)
        right_col = split.column(align=True)

        # put the toggle on the left col
        left_col_row = left_col.row(align=True)
        left_col_row.alignment = "RIGHT"  # alignment first!
        left_col_row.prop(
            context.scene.random_cube_props, "seed_toggle", icon_only=True
        )
        left_col_row.label(text="Set random seed")

        # put field in right col
        right_col.enabled = (
            context.scene.random_cube_props.seed_toggle
        )  # only disable the next part of the row
        right_col.prop(context.scene.random_cube_props, "seed")
        # alternative:
        # row = self.layout.row(align=True)
        # row.prop(context.scene.random_cube_props, "seed_toggle")

        # add a button for the operator
        row = self.layout.row(align=True)
        row.operator("object.add_random_cube", text="Add random cube")


# #-------------------------------
# Define function to append operator to menu's methods
# def menu_func(self, context):
#     # self.layout is a bpy.types.UILayout
#     # operator:
#     # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.operator
#     self.layout.operator(AddRandomCube.bl_idname)

# --------------------------------------------------
# Register and unregister functions:
list_classes_to_register = [
    PropertiesAddRandomMaterial,
    PanelAddRandomMaterial,
    AddRandomMaterial,
]


def register():
    """This is run when the add-on is enabled"""

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
        # add custom props to the scene! before registering the rest?
        if cls == PropertiesAddRandomMaterial:
            bpy.types.Scene.random_cube_props = bpy.props.PointerProperty(
                type=PropertiesAddRandomMaterial
            )
            # alternative: setattr(bpy.types.Scene, prop_name, prop_value)?

    # Adds the new operator to an existing menu.
    # bpy.types.VIEW3D_MT_object.append(menu_func)

    print("registered")


def unregister():
    """
    This is run when the add-on is disabled / Blender closes
    """
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    # delete the custom property pointer
    # NOTE: this is different from its accessor, as that is a read/write only
    # to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.random_cube_props

    # Remove the operator from existing menu.
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    print("unregistered")


# -------------------------------
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
# if __name__ == "__main__":
#     register()
