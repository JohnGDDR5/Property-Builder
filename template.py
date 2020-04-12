
## Operator Template
"""
class PROP_BUILDER_OT_ui_operators_move(bpy.types.Operator):
    bl_idname = "prop_builder.ui_ops_move"
    bl_label = "List Operators"
    bl_description = "Operators for moving rows Up, Down and Deleting"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    sub: bpy.props.StringProperty(default="DEFAULT")
    # index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.PPBR_Props
        active = props.ULIndex_Names
        
            
        
        # Resets self props into "DEFAULT"
        self.type == "DEFAULT"
        self.sub == "DEFAULT"
        
        return {'FINISHED'}
"""

## THIS ONE ISNT USED
"""
class PROP_BUILDER_collection_objects(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property Name", default="")
    prefix: bpy.props.StringProperty(name="Prefix", default="")
    collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    
    # duplicates: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    
    recent: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    custom: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    icon: bpy.props.StringProperty(name="Icon name for object", description="Used to display in the list", default="QUESTION")# , get=)# , update=checkIcon)
"""

# collection: bpy.props.CollectionProperty(name="Added Collections to List", type=PROP_BUILDER_property_string_booleans)

# collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
# object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)