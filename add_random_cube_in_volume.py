# A commented template for making simple UI in blender using the bpy python API: https://gist.github.com/tin2tin/ce4696795ad918448dfbad56668ed4d5
# https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663

### Imports
import bpy  # Python API
import numpy as np

#---------------------
### Add-on metadata
# https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo
bl_info = {
    "name": "Add random cube",
    "blender": (3,4,1), # min required version; get from running bpy.app.version
    "category": "Object",
    # optional
    'version': (1, 0, 0),
    'author': 'Sofia Miñano',
    'description': 'Add a unit cube at a random location within a cubic volume centred around the origin',
}



#---------------------------
# Properties
# create a property group, this is REALLY needed so that operators
#AND the UI can access, display and expose it to the user 
class PropertiesAddRandomCube(bpy.types.PropertyGroup): #---these will be added to context.scene.random_cube_props in registration
    vol_size: bpy.props.IntProperty(name='Target volume size', default=1, soft_min=0, soft_max=10)
    seed_toggle: bpy.props.BoolProperty(name='Set random seed', default=False)
    seed: bpy.props.IntProperty(name='Seed', default=42)


#-------
# Panel
class PanelAddRandomCube(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_add_random_cube'
    bl_label = 'Add random cube' # title of the panel / label displayed to the user
    bl_space_type = 'PROPERTIES' # see: https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items
    bl_region_type = 'WINDOW' # see full list: https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items
    

    def draw(self,context):

        ## Add multiple items in the same column
        # col = self.layout.column()
        # col.prop(context.scene.random_cube_props, "vol_size")
        # col.prop(context.scene.random_cube_props, "seed_toggle")
        # col.prop(context.scene.random_cube_props, "seed")

        ## Add a new row
        row = self.layout.row()
        row.prop(context.scene.random_cube_props, "vol_size")
        
        row = self.layout.row(align=True)
        row.prop(context.scene.random_cube_props, "seed_toggle")

        subrow = row.row()
        subrow.enabled = context.scene.random_cube_props.seed_toggle # only disable the next part of the row
        subrow.prop(context.scene.random_cube_props, "seed")
    

        # add a button for the operator
        row = self.layout.row(align=True)
        row.operator('object.add_random_cube', text = 'Add random cube')
        


#-------------------------------
## Operator
# must include some mandatory properties and an execute fn
# If inputs are defined as class properties, then I can do this:
#   bpy.ops.object.add_random_cube('EXEC_DEFAULT', seed=0, vol_size=1)
class AddRandomCube(bpy.types.Operator): #---check types
    """Add a random cube within a predefined volume"""  # this shows as a tooltip for menu items and buttons.

    #-------------------------------
    ### Props --why not in init?
    # Mandatory settings as class variables
    bl_idname = "object.add_random_cube"        # this is appended to bpy.ops.
    bl_label = "Add random cube in volume"      # Display name in the interface (this is how it shows in operator search)
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    #-------------
    #this is needed to check if the operator can be executed/invoked
    #in the current context  
    @classmethod
    def poll(cls, context):
        #check the context here
        return context.object is not None
    
    # ----------------------
    ## Invoke
    # runs before execute, to initialise ....?
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    #-------------------------------
    ### Execute fn
    def execute(self, context):

        # print(self.properties)

        # add a cube primitive and link it to the scene collection
        bpy.ops.mesh.primitive_cube_add() # returns {'FINISHED'} if successful
        cube_object = context.object

        # get inputs
        # seed: If None, then fresh, unpredictable entropy will be pulled from the OS.
        scene = context.scene
        seed = scene.random_cube_props.seed if scene.random_cube_props.seed_toggle else None
        vol_size = scene.random_cube_props.vol_size

        # set location randomly within predifined volume
        rng = np.random.default_rng(seed) # recommended constructor for the random number class Generator
        cube_object.location = vol_size*rng.random((3,)) - 0.5*vol_size

        return {'FINISHED'}


# #-------------------------------
# Define function to append operator to menu's methods
# def menu_func(self, context):
#     # self.layout is a bpy.types.UILayout
#     # operator:
#     # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.operator
#     self.layout.operator(AddRandomCube.bl_idname) # what is self here exactly?

#-------------------------------
# Register and unregister functions:
# Everything here is run when addon is enabled
# - registering the add-on class
# - appending 'draw function
list_classes_to_register = [
    PropertiesAddRandomCube, 
    PanelAddRandomCube, 
    AddRandomCube
]

def register():
    '''This is run when the add-on is enabled'''

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)  
        # add custom props to the scene! before registering the rest?
        if cls == PropertiesAddRandomCube:
            bpy.types.Scene.random_cube_props = bpy.props.PointerProperty(type=PropertiesAddRandomCube)
            # alternative: setattr(bpy.types.Scene, prop_name, prop_value)?

    # Adds the new operator to an existing menu.
    # bpy.types.VIEW3D_MT_object.append(menu_func)  

    print('registered')

def unregister():
    '''This is run when the add-on is disabled (or when Blender is shut down?)'''
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)

    #delete the custom property pointer
    #NOTE: this is different from its accessor, as that is a read/write only
    #to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.random_cube_props 

    # Remove the operator from existing menu.
    # bpy.types.VIEW3D_MT_object.remove(menu_func)  # remove! otherwise stays in the menu when uninstalled or disabled.... the new operator to an existing menu.
    print('unregistered') 

#-------------------------------
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()