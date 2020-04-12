bl_info = {
    "name": "Property Builder",
    "description": "Workflow Addon for easily updating, creating and managing multiple custom properies for rigs. Made for riggers.",
    "author": "Juan Cardenas (JohnGDDR5)",
    "version": (1, 0, 0), 
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar > Rig Property Manager",
    "warning": "In Development",
    "support": "COMMUNITY",
    "category": "Scene"
}

import bpy

import ast # For string to dictionary evaluations

#Imports Blender Properties ex. BoolProperty
from bpy.props import *

#from . backup_objects_addon_b2_80_v1_0_1 import classes
from . property_builder_b2_80_v1_0_0 import (
    PROP_BUILDER_properties,
    PROP_BUILDER_property_names,
    PROP_BUILDER_props,

    PROP_BUILDER_OT_general_ui_ops,
    
    PROP_BUILDER_OT_copy_paste_prop,
    PROP_BUILDER_OT_generate_custom_props,

    PROP_BUILDER_UL_items_strings,
    PROP_BUILDER_UL_items_properties,
    
    PROP_BUILDER_MT_dropdown_menu_ui_generate,
    PROP_BUILDER_MT_dropdown_menu_ui_properties,
    
    PROP_BUILDER_PT_custom_panel1,
    PROP_BUILDER_PT_property_editor,
    PROP_BUILDER_PT_options,

    PROP_BUILDER_preferences
)

#print("classes"+str(classes) )
#Yes, I had to do this or else it would not register correctly
classes = (
    PROP_BUILDER_properties,
    PROP_BUILDER_property_names,
    PROP_BUILDER_props,

    PROP_BUILDER_OT_general_ui_ops,
    
    PROP_BUILDER_OT_copy_paste_prop,
    PROP_BUILDER_OT_generate_custom_props,

    PROP_BUILDER_UL_items_strings,
    PROP_BUILDER_UL_items_properties,
    
    PROP_BUILDER_MT_dropdown_menu_ui_generate,
    PROP_BUILDER_MT_dropdown_menu_ui_properties,
    
    PROP_BUILDER_PT_custom_panel1,
    PROP_BUILDER_PT_property_editor,
    PROP_BUILDER_PT_options,

    PROP_BUILDER_preferences
)

def register():
    #ut = bpy.utils
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.PPBR_Props = bpy.props.PointerProperty(type=PROP_BUILDER_props)
    
def unregister():
    #ut = bpy.utils
    #from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    #Just incase to prevent an error
    if hasattr(bpy.types.Scene, "PPBR_Props") == True:
        del bpy.types.Scene.PPBR_Props
    
#register, unregister = bpy.utils.register_classes_factory(classes)
if __name__ == "__main__":
    register()
