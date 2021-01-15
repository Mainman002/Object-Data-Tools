import bpy


bl_info = {
    "name": "Object_Data_Tools",
    "author": "Johnathan Mueller",
    "descrtion": "A panel that helps with various object data operations.",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > Edit Tab",
    "warning": "",
    "category": "Object"
}



class OBJECT_OT_Object_Data_Make_Copy(bpy.types.Operator):
    bl_idname = 'obj.make_copy'
    bl_label = 'Copy'
    bl_description = 'Copies active object data to selected objects'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
    
        active_ob = bpy.context.active_object
        selected_obs = bpy.context.selected_objects
        
        for obj in selected_obs:
            if obj.type == active_ob.type:
                obj.data = active_ob.data

        return {'FINISHED'}
    
    
    
class OBJECT_OT_Object_Data_Make_Unique(bpy.types.Operator):
    bl_idname = 'obj.make_unique'
    bl_label = 'Unique'
    bl_description = 'Duplicates object data of selected objects, then makes them unique'
    bl_options = {'REGISTER'}
       
    def execute(self, context):
        
        selected_obs = bpy.context.selected_objects
        
        for obj in selected_obs:
            new_obj = obj.copy()
            obj.data = new_obj.data.copy()

        return {'FINISHED'}




class OBJECT_PT_Data_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_panel'
    bl_category = 'Object Data'
    bl_label = 'Mesh Data Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)            
            row.operator('obj.make_copy', icon='RESTRICT_INSTANCED_OFF')
            
            row.operator('obj.make_unique', icon='MESH_DATA')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')





classes = (
    OBJECT_PT_Data_Panel,
    OBJECT_OT_Object_Data_Make_Copy,
    OBJECT_OT_Object_Data_Make_Unique,
)



def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)


def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)


if __name__ == "__main__":
    register()
