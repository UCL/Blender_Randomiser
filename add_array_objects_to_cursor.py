
import bpy

#--------------------
# Metadata
bl_info ={
    "name": "Add array of objects to cursor",
    "blender": (3,4,1), # min required version; get from running bpy.app.version
    "category": "Object", # not sure what this determines
}


#---------------
# Properties
class PropertiesAddArrayObjects2Cursor(bpy.types.PropertyGroup):
    n_objects_array: bpy.props.IntProperty(
        name='Number of objects in array',
        default=10,
        description='Number of objects to generate between current active object and cursor',
        soft_min=0,
        soft_max=100,
    ) # annotation

# ---------------
# Operator
class AddArrayObjects2Cursor(bpy.types.Operator): # ---what other classes can I instantiate?

    ## Class properties 
    bl_idname = 'object.add_array_objects_to_cursor'
    bl_label = 'Add array of objects to cursor'
    bl_options = {'REGISTER', 'UNDO'} #---- what other?

    ## Execute fn
    def execute(self, context):
        scene = context.scene
        cursor_loc = scene.cursor.location
        object_active = context.active_object

        for i in range(scene.array_objects2cursor_props.n_objects_array):
            object_copy = object_active.copy() # copy to the same data block (linked copy)
            scene.collection.objects.link(object_copy)

            factor = i / scene.array_objects2cursor_props.n_objects_array
            object_copy.location = (object_active.location*factor) + (cursor_loc*(1.0 - factor))
        
        return {'FINISHED'}


#------------
# Panel
class PanelAddArrayObjects2Cursor(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_add_array_objects2cursor'
    bl_label = 'Add array of objects to cursor' # title of the panel / label displayed to the user
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    

    def draw(self,context):

        layout = self.layout
        row = layout.row()
        split = row.split()
        left_col = split.column(align=True)
        right_col = split.column(align=True)

        left_col.alignment='RIGHT'
        left_col.label(text='Number of objects in array') # TODO: can I get this from the property?
        right_col.prop(context.scene.array_objects2cursor_props, 
                        'n_objects_array',
                        icon_only=True)
        # self.layout.use_property_split = True
        # self.layout.use_property_decorate = False  # No animation.

        # add a button for the operator
        row = self.layout.row(align=True)
        row.operator('object.add_array_objects_to_cursor', text = 'Add array')
        

#-------------
# Register / Unregister classes
list_classes_to_register = [
    PropertiesAddArrayObjects2Cursor, 
    PanelAddArrayObjects2Cursor, 
    AddArrayObjects2Cursor
]    

def register():
    '''This is run when the add-on is enabled'''

    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)  
        if cls == PropertiesAddArrayObjects2Cursor:
            bpy.types.Scene.array_objects2cursor_props = bpy.props.PointerProperty(type=PropertiesAddArrayObjects2Cursor)

    print('registered')

def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)  

    # delete the custom property pointer
    del bpy.types.Scene.array_objects2cursor_props 

    print('unregistered') 


if __name__ == "__main__":
    register()
