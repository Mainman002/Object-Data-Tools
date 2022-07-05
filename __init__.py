import bpy, sys, os

from . TMG_Object_Data import *

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Extra online resources used in this script
# https://blender.stackexchange.com/questions/155515/how-do-a-create-a-foldout-ui-panel

# Thank you all that download, suggest, and request features
# As well as the whole Blender community. You're all epic :)


bl_info = {
    "name": "TMG_Object_Data",
    "author": "Johnathan Mueller",
    "descrtion": "A panel that helps with various object data operations",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > TMG",
    "warning": "",
    "category": "Object"
}

classes = (
    ## Properties
    TMG_Object_Data_Properties,

    OBJECT_PT_TMG_OB_Data_Parent_Panel,
    OBJECT_PT_Scene_Data_Panel,
    OBJECT_PT_Data_Panel,
    OBJECT_PT_Data_Name_Panel,
    OBJECT_OT_Object_Data_Make_Copy,
    OBJECT_OT_Object_Data_Make_Unique,
    OBJECT_OT_Name_Active_To_Paintable_Low,
    OBJECT_OT_Name_Active_To_Paintable_High,
    OBJECT_OT_Name_Active_To_Paintable_None,
)

def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.tmg_object_data_vars = bpy.props.PointerProperty(type=TMG_Object_Data_Properties)

def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)

if __name__ == "__main__":
    register()

