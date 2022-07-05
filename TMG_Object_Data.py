import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty


def _change_ob(self, context, _ob):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = _ob
    _ob.select_set(True) 
    return _ob


def _get_ob_name(self):
    return self.get("ob_name", bpy.context.active_object.name)


def _set_ob_name(self, value):
    scene = bpy.context.scene
    tmg_object_data_vars = scene.tmg_object_data_vars
    ob = bpy.context.active_object

    if ob.name != value:
        ob.name = value

    if tmg_object_data_vars.ob_name_lock:
        if ob.data and ob.data.name != value:
            ob.data.name = value


def _get_ob_data_name(self):
    if bpy.context.active_object.data:
        return self.get("ob_data_name", bpy.context.active_object.data.name)


def _set_ob_data_name(self, value):
    scene = bpy.context.scene
    tmg_object_data_vars = scene.tmg_object_data_vars
    ob = bpy.context.active_object

    if ob.data.name != value:
        ob.data.name = value

    if tmg_object_data_vars.ob_name_lock:
        if ob.data and ob.data.name != value:
            ob.data.name = value


class TMG_Object_Data_Properties(bpy.types.PropertyGroup):
    ob_name_lock : bpy.props.BoolProperty(name='Linked Name', default=True)
    ob_name : bpy.props.StringProperty(name='Object', default='Object', set=_set_ob_name, get=_get_ob_name)
    ob_data_name : bpy.props.StringProperty(name='Data', default='Object', set=_set_ob_data_name, get=_get_ob_data_name)


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


def rename_selected(self, context, _name):
    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            if ob.name.rsplit('_',1)[-1] == 'low' or ob.name.rsplit('_',1)[-1] == 'high':
                to_pop = '_' + ob.name.rsplit('_',1)[-1]
                ob.name = ob.name.strip(to_pop)
                
            if ob.data.name.rsplit('_',1)[-1] == 'low' or ob.data.name.rsplit('_',1)[-1] == 'high':
                to_pop = '_' + ob.data.name.rsplit('_',1)[-1]
                ob.data.name = ob.data.name.strip(to_pop)
            
            ob.name = ob.name + '_' + _name
            ob.data.name = ob.data.name + '_' + _name
        

def rename_selected_none(self, context):
    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            if ob.name.rsplit('_',1)[-1] == 'low' or ob.name.rsplit('_',1)[-1] == 'high':
                to_pop = '_' + ob.name.rsplit('_',1)[-1]
                ob.name = ob.name.strip(to_pop)
                
            if ob.data.name.rsplit('_',1)[-1] == 'low' or ob.data.name.rsplit('_',1)[-1] == 'high':
                to_pop = '_' + ob.data.name.rsplit('_',1)[-1]
                ob.data.name = ob.data.name.strip(to_pop)


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


class OBJECT_PT_TMG_OB_Data_Parent_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_tmg_ob_data_parent_panel'
    bl_category = 'TMG'
    bl_label = 'Data Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout


class OBJECT_PT_Scene_Data_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_scene_data_panel'
    bl_label = 'Scene Data'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "OBJECT_PT_tmg_ob_data_parent_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        ## My Panel Operator 
        prop = layout.operator('outliner.orphans_purge', icon='RESTRICT_INSTANCED_OFF')
        prop.do_local_ids=True
        prop.do_linked_ids=True
        prop.do_recursive=True
        
        col = layout.column()


class OBJECT_PT_Data_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_panel'
    bl_label = 'Mesh Data'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "OBJECT_PT_tmg_ob_data_parent_panel"
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        scene = context.scene
        layout = self.layout


        if bpy.context.selected_objects:
            row = layout.row(align=True)            
            row.operator('obj.make_copy', icon='RESTRICT_INSTANCED_OFF')
            
            row.operator('obj.make_unique', icon='MESH_DATA')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()
        

class OBJECT_PT_Data_Name_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_data_name_panel'
    bl_label = 'Mesh Name'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "OBJECT_PT_tmg_ob_data_parent_panel"
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        scene = context.scene
        tmg_object_data_vars = scene.tmg_object_data_vars
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)
            row.operator('wm.object_ot_name_active_to_paintable_none', icon='OUTLINER_OB_FONT')
            row = layout.row(align=True)         
            row.operator('wm.object_ot_name_active_to_paintable_low', icon='OUTLINER_OB_FONT')
            row.operator('wm.object_ot_name_active_to_paintable_high', icon='OUTLINER_OB_FONT')

            col = layout.column(align=True)
            col.prop(tmg_object_data_vars, 'ob_name_lock')
            
            if tmg_object_data_vars.ob_name_lock:
                col.prop(tmg_object_data_vars, 'ob_name')
            else:
                col.prop(tmg_object_data_vars, 'ob_name')

                if bpy.context.active_object.data != None:
                    col.prop(tmg_object_data_vars, 'ob_data_name')

        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')

        col = layout.column()

