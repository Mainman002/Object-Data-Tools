import bpy


bl_info = {
    "name": "Object_Data_Tools",
    "author": "Johnathan Mueller",
    "descrtion": "A panel that helps with various object data operations.",
    "blender": (2, 80, 0),
    "version": (0, 1, 2),
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


def _mesh_name(ob):
    if ob.name.rsplit('_',1)[-1] == 'low' or ob.name.rsplit('_',1)[-1] == 'high':
        to_pop = '_' + ob.name.rsplit('_',1)[-1]
        ob.name = ob.name.strip(to_pop)
    return {'FINISHED'}

def _mesh_data_name(ob):
    if ob.data.name.rsplit('_',1)[-1] == 'low' or ob.data.name.rsplit('_',1)[-1] == 'high':
        to_pop = '_' + ob.data.name.rsplit('_',1)[-1]
        ob.data.name = ob.data.name.strip(to_pop)
    return {'FINISHED'}


def rename_selected(self, context, _name):
    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            _mesh_name(ob)
            _mesh_data_name(ob)
            
            ob.name = ob.name + '_' + _name
            ob.data.name = ob.data.name + '_' + _name
    return {'FINISHED'}
        

def rename_selected_none(self, context):
    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            _mesh_name(ob)
            _mesh_data_name(ob)
    return {'FINISHED'}


def remove_unused_materials(self, context, _ob):
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = _ob
    _ob.select_set(state=True)
    bpy.ops.object.material_slot_remove_unused()
    return {'FINISHED'}


class OBJECT_OT_Name_Active_To_Paintable_None(bpy.types.Operator):
    bl_idname = 'wm.object_ot_name_active_to_paintable_none'
    bl_label = 'Remove'
    bl_description = 'Renames objects to active object without a name extention.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        rename_selected_none(self, context)
        return {'FINISHED'}




class OBJECT_OT_Name_Active_To_Paintable_Low(bpy.types.Operator):
    bl_idname = 'wm.object_ot_name_active_to_paintable_low'
    bl_label = '_low'
    bl_description = 'Renames objects to active object with _low name extentions.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        rename_selected(self, context, 'low')
        return {'FINISHED'}



class OBJECT_OT_Name_Active_To_Paintable_High(bpy.types.Operator):
    bl_idname = 'wm.object_ot_name_active_to_paintable_high'
    bl_label = '_high'
    bl_description = 'Renames objects to active object with _high name extentions.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        rename_selected(self, context, 'high')
        return {'FINISHED'}



class OBJECT_OT_Material_Active_To_Selected(bpy.types.Operator):
    bl_idname = 'wm.object_ot_material_active_to_selected'
    bl_label = 'Materials'
    bl_description = 'Copy materials to other objects.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        bpy.ops.object.material_slot_copy()
        return {'FINISHED'}
    
    
class OBJECT_OT_Modifier_Active_To_Selected(bpy.types.Operator):
    bl_idname = 'wm.object_ot_modifier_active_to_selected'
    bl_label = 'Modifiers'
    bl_description = 'Copy modifiers to other objects.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        bpy.ops.object.make_links_data(type='MODIFIERS')
        return {'FINISHED'}


class OBJECT_OT_Remove_Unused_Materials(bpy.types.Operator):
    bl_idname = 'wm.object_ot_remove_unused_materials'
    bl_label = 'Unused Materials'
    bl_description = 'Remove unused materials on selected objects'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            if ob.type == "MESH":
                remove_unused_materials(self, context, ob)
        return {'FINISHED'}


class OBJECT_PT_Data_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_panel'
    bl_category = 'Object Data'
    bl_label = 'Mesh Data'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        myscene = context.scene
        layout = self.layout


        if bpy.context.selected_objects:
            row = layout.row(align=True)            
            row.operator('obj.make_copy', icon='RESTRICT_INSTANCED_OFF')
            
            row.operator('obj.make_unique', icon='MESH_DATA')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()


class OBJECT_PT_Data_Copy_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_copy_panel'
    bl_category = 'Object Data'
    bl_label = 'Copy'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        myscene = context.scene
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)
            row.operator('wm.object_ot_material_active_to_selected', icon='MATERIAL')
            row.operator('wm.object_ot_modifier_active_to_selected', icon='MODIFIER')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()


class OBJECT_PT_Data_Name_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_name_panel'
    bl_category = 'Object Data'
    bl_label = 'Name'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        myscene = context.scene
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)
            row.operator('wm.object_ot_name_active_to_paintable_none', icon='OUTLINER_OB_FONT')
            row = layout.row(align=True)         
            row.operator('wm.object_ot_name_active_to_paintable_low', icon='OUTLINER_OB_FONT')
            row.operator('wm.object_ot_name_active_to_paintable_high', icon='OUTLINER_OB_FONT')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()


class OBJECT_PT_Cleanup_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_cleanup_panel'
    bl_category = 'Object Data'
    bl_label = 'Remove'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        myscene = context.scene
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)
            row.operator('wm.object_ot_remove_unused_materials', icon='MATERIAL')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()





classes = (
    OBJECT_PT_Data_Panel,
    OBJECT_PT_Data_Copy_Panel,
    OBJECT_PT_Data_Name_Panel,
    OBJECT_PT_Cleanup_Panel,
    OBJECT_OT_Object_Data_Make_Copy,
    OBJECT_OT_Object_Data_Make_Unique,
    OBJECT_OT_Name_Active_To_Paintable_Low,
    OBJECT_OT_Name_Active_To_Paintable_High,
    OBJECT_OT_Name_Active_To_Paintable_None,
    OBJECT_OT_Material_Active_To_Selected,
    OBJECT_OT_Modifier_Active_To_Selected,
    OBJECT_OT_Remove_Unused_Materials,
)



def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)


def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)


if __name__ == "__main__":
    register()