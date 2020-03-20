
bl_info = {
    "name": "Rig Property Manager",
    "description": "Workflow Addon for easily updating, creating and managing multiple custom properies for rigs. Made for riggers.",
    "author": "Juan Cardenas (JohnGDDR5)",
    "version": (1, 0, 1), 
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar > Rig Property Manager",
    "warning": "In Development",
    "support": "COMMUNITY",
    "category": "Scene"
}


import bpy
        
from bpy.props import *
    
#Takes in an object as parameter, and returns a string of variable "icon"
def objectIcon(object):
    scene = bpy.context.scene
    data = bpy.data
    props = scene.RPMR_Props
    
    #icons = ["OUTLINER_OB_EMPTY", "OUTLINER_OB_MESH", "OUTLINER_OB_CURVE", "OUTLINER_OB_LATTICE", "OUTLINER_OB_META", "OUTLINER_OB_LIGHT", "OUTLINER_OB_IMAGE", "OUTLINER_OB_CAMERA", "OUTLINER_OB_ARMATURE", "OUTLINER_OB_FONT", "OUTLINER_OB_SURFACE", "OUTLINER_OB_SPEAKER", "OUTLINER_OB_FORCE_FIELD", "OUTLINER_OB_GREASEPENCIL", "OUTLINER_OB_LIGHTPROBE"]
    #Object Type
    
    icon = "QUESTION"
    
    #schema: "Object Type": "Icon Name"
    dictionary = {
        "MESH": "OUTLINER_OB_MESH",
        "EMPTY": "EMPTY",
        "CAMERA": "OUTLINER_OB_CAMERA",
        "CURVE": "OUTLINER_OB_CURVE",
        "SURFACE": "OUTLINER_OB_SURFACE",
        "META": "OUTLINER_OB_META",
        "FONT": "OUTLINER_OB_FONT",
        "GPENCIL": "OUTLINER_OB_GREASEPENCIL",
        "ARMATURE": "OUTLINER_OB_ARMATURE",
        "LATTICE": "OUTLINER_OB_LATTICE",
        "LIGHT": "OUTLINER_OB_LIGHT",
        "LIGHT_PROBE": "OUTLINER_OB_LIGHTPROBE",
        "SPEAKER": "OUTLINER_OB_SPEAKER",
    }
    
    #If there is an object to see if it has a type
    if object is not None:
        type = object.type
    
        icon = dictionary.get(str(type), "QUESTION")
        
        if icon == "EMPTY":
            if object.empty_display_type != "IMAGE":
                icon = "OUTLINER_OB_EMPTY"
            elif object.empty_display_type == "IMAGE":
                icon = "OUTLINER_OB_IMAGE"
            elif object.field.type != "NONE":
                icon = "OUTLINER_OB_FORCE_FIELD"
                
    return icon

##General UI Functions & Operators - TOP

#Copies properties from one object to another. If Duplicate Object is missing properties, it will ignore it.
def copyAttributes(object, object_duplicate):
    attributes = []
    bruh = []
    ignore = ('bl_rna', 'rna_type')
    missing = []
    #For loop to only get the attributes I made, not the default python and blender ones
    for i in dir(object):
        if i.startswith('__') == False and (i not in ignore):
            attributes.append(i)
        else:
            bruh.append(i)
            
    print("bruh: %s" % (str(bruh) ) )
    print("attributes: %s" % (str(attributes) ) )
    
    for i in attributes:
        if hasattr(object_duplicate, i):
            original_attr = getattr(object, i)
            setattr(object_duplicate, i, original_attr)
        else:
            missing.append(i)
    
    #Prints the missing attributes for debugging
    if len(missing) > 0:
        class_name = object_duplicate.__class__.__name__
        print("%s missing %d attributes: %s" % (class_name, len(missing), str(missing) ) )

def UI_Functions(collection, UI_Index, type):
    #collection is for ex. props.strings
    #UI_Index is the index of active UI list element
    col = collection
    #gets the last index of list
    list_length = len(col)-1
    print("UI_Index[1]: %d" % (UI_Index) )
    #Add new item to collection
    if type == "ADD":
        col.add()
        UI_Index = len(col)-1
        #if len(col)
    #Basically Deletes
    elif type == "REMOVE":
        col.remove(UI_Index)
        if UI_Index >= list_length:
            UI_Index -= 1
    #Moves up
    elif type == "UP":
        if UI_Index != 0:
            col.move(UI_Index, UI_Index-1)
            UI_Index -= 1
        else:
            col.move(UI_Index, list_length)
            UI_Index = list_length
    #Moves down
    elif type == "DOWN":
        if UI_Index != list_length:
            col.move(UI_Index, UI_Index+1)
            UI_Index += 1
        else:
            col.move(UI_Index, 0)
            UI_Index = 0
    #Creates a Duplicate of the object in the collection
    elif type == "DUPLICATE":
        if list_length >= 0:
            duplicate = col.add()
            copyAttributes(col[UI_Index], duplicate)
            
        
    print("UI_Index[1]: %d" % (UI_Index) )
    return int(UI_Index)

class REGEX_SCANNER_OT_General_UIOps(bpy.types.Operator):
    bl_idname = "regex_scanner.general_ui_ops"
    bl_label = "General UI List Operators/Functions"
    bl_description = "For adding, removing and moving up/down list elements"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    collection: bpy.props.StringProperty(default="DEFAULT")
    list_index: bpy.props.StringProperty(default="DEFAULT")
    #include: bpy.props.BoolProperty(default=False)
    #mirror: bpy.props.BoolProperty(default=False)
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    #Resets default settings
    #@classmethod
    @staticmethod
    def resetSelf(self):
        self.type = "DEFAULT"
        self.collection = "DEFAULT"
        self.list_index = "DEFAULT"
        print("Reset States: %s, %s, %s" % (self.type, self.collection, self.list_index) )
        #return None
        
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")
    
    @classmethod #This one seems useless
    def poll(cls, context):
        #return cls.collection != "DEFAULT"
        #print("cls.collection: %s" % (str(cls.collection)) )
        #return collection != "DEFAULT"
        return True
    
    #Use for later
    #Checks if object has attribute and returns it, else returns None
    #@staticmethod #Uncomment this after adding it
    def returnAttribute(self, object, attributeString):
        if hasattr(object, attributeString):
            return getattr(object, attributeString)
        else:
            return None
    
    def execute(self, context):
        scene = bpy.context.scene
        #context = bpy.context
        data = context.object.data
        props = scene.RPMR_Props
        
        reportString = "Done!"
        
        collection = self.returnAttribute(props, self.collection)
        UI_Index = self.returnAttribute(props, self.list_index)
        
        if collection != None:
            #Need != None, as "if" returns False if number is "0"
            if UI_Index != None:
                #props.RS_ULIndex_ReGex = UI_Functions(self.collection, self.list_index, self.type)
                
                print("UI_Index[1]: %d" % (UI_Index) )
                #getattr(props, self.list_index) = UI_Functions(collection, UI_Index, self.type)
                #UI_Index = UI_Functions(collection, UI_Index, self.type)
                setattr(props, self.list_index, UI_Functions(collection, UI_Index, self.type) )
                print("UI_Index[2]: %d" % (UI_Index) )
            else:
                print("UI_Index[3]: %d" % (UI_Index) )
                reportString = "List_Index given wasn't found in scene.RPMR_Props"
        else:
            reportString = "Collection given wasn't found in scene.RPMR_Props"
        #Resets default settings
        self.resetSelf(self)
        
        print(reportString)
        self.report({'INFO'}, reportString)
        
        return {'FINISHED'}

##General UI Functions & Operators - TOP

class RIG_PROP_MAN_OT_select_collection(bpy.types.Operator):
    bl_idname = "rig_prop_man.select_collection"
    bl_label = "Select Collection"
    bl_description = "Sets Parent collection for Backups"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=-1)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
                
        if self.type == "SELECT_ACTIVE":
            props.collection_active = bpy.data.collections[self.index]
            
        self.type == "DEFAULT"
        
        return {'FINISHED'}

class RIG_PROP_MAN_OT_group_operators(bpy.types.Operator):
    bl_idname = "rig_prop_man.collection_ops"
    bl_label = "Create a new Collection"
    bl_description = "Creates a new Parent Collection where new Backup collections for Objects are created."
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
        
        #New Collection Group inside Parent Collection and set as Active Collection
        if self.type == "NEW_GROUP":
            
            colNew = bpy.data.collections.new(props.group_name)
            #Links colNew2 to collection_active
            props.collection_active = colNew
            
            #Links new collection to Master_Collection
            bpy.context.scene.collection.children.link(colNew)
            
            #Note for For Loop Bellow: For every props.collections[].collection, create a new collection and set that as the pointer to the collections[].collection so each object gets a new collection
            
            #Removes collections from all RPMR_Props.collections.collection
            for i in enumerate(props.collections):
                i[1].collection = None
                
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
#Note: This must be updated to actually be a debugger for the new addon
class RIG_PROP_MAN_OT_debugging(bpy.types.Operator):
    bl_idname = "rig_prop_man.debug"
    bl_label = "Backup Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO','REGISTER'}
    type: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def invoke(self, context, event):
        #self.x = event.mouse_x
        #self.y = event.mouse_y
        if self.type != "DELETE_NUKE":
            return self.execute(context)
        else:
            print("MLG")
            wm = context.window_manager
            print(str(event))
            #invoke_props_popup(operator, event)
            #return wm.invoke_props_dialog(self)
            return wm.invoke_confirm(self, event)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
        
        #Mass deletion of every Iteration Object & their collections and objects inside them
        if self.type == "DELETE_NUKE":
            
            if props.collection_active is not None:
                removedObjects = 0
                removedCol = 0
                
                for i in enumerate(reversed(props.collections)):
                    if i[1].collection is not None:
                        for j in i[1].collection.objects:
                            removedObjects += 1
                            i[1].collection.objects.unlink(j)
                            
                        removedCol += 1
                        #Removes collection, but not other links of it incase the user linked it
                        bpy.data.collections.remove(i[1].collection, do_unlink=True)
                        
                    props.collections.remove(len(props.collections)-1)
                    
                colNameActive = props.collection_active.name
                    
                reportString = "Removed: [%s] & %d Objects & %d Collection Groups" % (colNameActive, removedObjects, removedCol)
                
                bpy.data.collections.remove(props.collection_active, do_unlink=True)
                
                print(reportString)
                self.report({'INFO'}, reportString)
            else:
                #Removes scene.RPMR_Props.collections
                for i in enumerate(reversed(props.collections)):
                    props.collections.remove(len(props.collections)-1)
                
            print(reportString)
            self.report({'INFO'}, reportString)
                
        elif self.type == "PRINT_1":
            no_objects = 0
            no_collections = 0
            
            for i in enumerate(props.collections):
                if i[1].object != None:
                    print_ob = str(i[1].object.name)
                else:
                    print_ob = "[None]"
                    no_objects += 1
                    
                if i[1].collection != None:
                    print_col = str(i[1].collection.name)
                else:
                    print_col = "[None]"
                    no_collections += 1
                
                print("%d. Object: %s, Collection: %s" % (i[0], print_ob, print_col))
                
            print("Total Objects: %d" % (len(props.collections)))
            #Displays how many Iteration Objects don't have Objects or Collections
            print("No Objects: %d; No Collections: %d" % (no_objects, no_collections))
        
        #Adds 3 Backup Objects with missing Objects & Collections for testing.
        elif self.type == "TESTING":
            
            ob_1 = props.collections.add()
            ob_1.collection = bpy.data.collections[0]
            
            ob_2 = props.collections.add()
            ob_2.object = bpy.data.objects[0]
            
            ob_3 = props.collections.add()
            print("Added 3 Backup Objects.")
            
        #Copied from .remove_ops operator before.
        elif self.type == "PRINT":
            #Gets previous length of props.collections
            len_previous = len(props.collections)
            
            before = list(props.collections)
            
            for i in reversed(list(enumerate(before))):
                if len(i[1].collection.objects) == 1:
                    print("before[i[0]]: [%d]; Object.name: %s" % (i[0], before[i[0]].object.name))
                    del before[i[0]]
            
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
class RIG_PROP_MAN_OT_ui_operators_move(bpy.types.Operator):
    bl_idname = "rig_prop_man.ui_ops_move"
    bl_label = "List Operators"
    bl_description = "Operators for moving rows Up, Down and Deleting"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
        active = props.RPMN_ULIndex
        
        #collection_active: 
        #collections:
            #collection:
            #object:
            #duplicates:
            #recent:
            
        
        #Moves list row UP
        if self.type == "UP":
            
            if self.sub == "DEFAULT":
                if active != 0:
                    props.collections.move(active, active-1)
                    props.RPMN_ULIndex-=1
                    
                else:
                    props.collections.move(0, len(props.collections)-1)
                    props.RPMN_ULIndex  = len(props.collections)-1
                    
            elif self.sub == "TOP":
                props.collections.move(active, 0)
                props.RPMN_ULIndex = 0
        
        #Moves list row DOWN
        elif self.type == "DOWN":
            
            if self.sub == "DEFAULT":
                if active != len(props.collections)-1:
                    props.collections.move(active, active+1)
                    props.RPMN_ULIndex += 1
                    
                else:
                    props.collections.move(len(props.collections)-1, 0)
                    props.RPMN_ULIndex = 0
                    
            elif self.sub == "BOTTOM":
                props.collections.move(active, len(props.collections)-1)
                props.RPMN_ULIndex = len(props.collections)-1
                
        elif self.type == "REMOVE" and len(props.collections) > 0:
        
            if self.sub == "DEFAULT":
                #If active is the last one
                if active == len(props.collections)-1:
                    props.collections.remove(props.RPMN_ULIndex)
                    
                    if len(props.collections) != 0:
                        props.RPMN_ULIndex -= 1
                        
                else:
                    props.collections.remove(props.RPMN_ULIndex)
            #Note: This only removes the props.collections, not the actual collections or 
            """
            elif self.sub == "ALL":
                props.collections.clear()
            """
                
                
        #Note: This only removes the props.collections, not the actual collections or objects
        elif self.type == "REMOVE_UI_ALL":
            props.collections.clear()
            
            reportString = "Removed all UI List elements. (Objects in Scene unaffected)" #% (active_object.name)
            
            self.report({'INFO'}, reportString)
                
        elif self.type == "SELECT_ACTIVE_UI":
            active_object = bpy.context.active_object
            if active_object != None:
                found = False
                
                for i in enumerate(props.collections):
                    if active_object == i[1].object:
                        props.RPMN_ULIndex = i[0]
                        found = True
                        break
                        
                if found == False:
                    reportString = "\"%s\" not in Iteration List" % (active_object.name)
                    
                    self.report({'INFO'}, reportString)
            else:
                reportString = "No Active Object"
                    
                self.report({'INFO'}, reportString)
            
        
        #Resets self props into "DEFAULT"
        self.type == "DEFAULT"
        self.sub == "DEFAULT"
        
        return {'FINISHED'}

#List drawing Class
class RIG_PROP_MAN_UL_items(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        #active = props.RIA_ULIndex
        RPMR_Collection = props.collections
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(RPMR_Collection) > 0:
                #obItems
                if item.collection != None:
                    obItems = len(item.collection.objects)
                else:
                    obItems = 0
                
                #info = "%d. (%d)" % (index+1, obItems)
                info = ""
                #info = "%d. (%d)" % (index+1, obItems)
                if props.display_index == True:
                    if props.display_object_count == True:
                        info += "%d. " % (index+1)
                    else:
                        info += "%d" % (index+1)
                    
                if props.display_object_count == True:
                    info += "(%d)" % (obItems)
                #bpy.context.scene.RPMR_Props.collections.add()
                
                #Displays icon of objects in list
                if props.display_icons == True:
                    
                    if item.object != "EMPTY" and item.icon != "NONE":
                        row.label(text="", icon=item.icon)
                        
                    else:
                        #obIcon = objectIcon(item.object)
                        row.label(text="", icon="QUESTION")
                        
                #Checks if the item has an object pointed
                if item.object != None:
                    row.prop(item.object, "name", text=info, emboss=False)
                    
                else:
                    col = row.column()
                    #Grays this out
                    col.enabled = False
                    
                    col.prop(props, "error_object", text=info, emboss=False)
                
                if props.display_collections == True:
                    if item.collection != None:
                        row.prop(item.collection, "name", text="", icon="GROUP", emboss=False)
                        
                    else:
                        col = row.column()
                        #Grays this out
                        col.enabled = False
                        
                        col.prop(props, "error_collection", text="", icon="GROUP", emboss=False)
                    
            else:
                row.label(text="No Iterations Here")
                
        #Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass
        
"""
class RIG_PROP_MAN_MT_menu_select_collection(bpy.types.Menu):
    bl_idname = "RIG_PROP_MAN_MT_menu_select_collection"
    bl_label = "Select a Collection for Active"
    bl_description = "Select an Parent Collection to create collections to send object iteration duplicates"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        col = layout.column()
        
        row = col.row(align=True)
        
        if len(bpy.data.collections) > 0:
            for i in enumerate(bpy.data.collections):
                button = row.operator("rig_prop_man.select_collection", text=i[1].name)
                button.type = "SELECT_ACTIVE"
                button.index = i[0]
                
                row = col.row(align=True)
        else:
            #NEW_COLLECTION
            button = row.operator("rig_prop_man.collection_ops", text="Add Collection", icon = "ADD")
            button.type = "NEW_COLLECTION"
            #bpy.data.collections.new("Boi") 
        #row.prop(self, "ui_tab", expand=True)#, text="X")
"""
    
class RIG_PROP_MAN_PT_custom_panel1(bpy.types.Panel):
    #A Custom Panel in Viewport
    bl_idname = "RIG_PROP_MAN_PT_custom_panel1"
    bl_label = "Property Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    collectionOOF: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        scene = context.scene
        props = scene.RPMR_Props
        
        #Layout Starts
        col = layout.column()
        
        #Active Collection
        row = col.row(align=True)
        row.label(text="Custom Property Placement:")
        
        row = col.row(align=True)
        row.prop(props, "custom_prop_placement", expand=True)
        
        col.separator()
        
        row = col.row(align=True)
        row.label(text="Parent Collection:")
        
        row = col.row(align=True)
        
        MenuName2 = "Select Collection"
        
        if props.collection_active is not None:
            MenuName2 = props.collection_active.name
            
        #Lock Icon
        if props.lock_active == False:
            row.prop(props, "lock_active", icon="UNLOCKED", text="")
        else:
            row.prop(props, "lock_active", icon="LOCKED", text="")
            
        """
        #if props.collection_active is None:
        if props.lock_active == False or props.collection_active is None:
            if props.collection_active is None:
                row.menu("RIG_PROP_MAN_MT_menu_select_collection", icon="GROUP", text=MenuName2)
            else:
                row.prop(props, "collection_active", text="")#, icon="GROUP", text="")
        else:
            row.prop(props.collection_active, "name", icon="GROUP", text="")
        """
            
        row.operator("rig_prop_man.collection_ops", icon="ADD", text="").type = "NEW_GROUP"
        
        #Separates for extra space between
        col.separator()
        
        #Duplicate Button TOP
        if bpy.context.object != None:
            ob_name_1 = bpy.context.object.name
        else:
            ob_name_1 = "No Object Selected"
            
        #For Loop Checks if the active Object hasn't been Backed Up before
        ob_name_col_1 = "New Collection"
        #iterateNew is False if the Object/Collection has been Backed Up
        iterateNew = False
        
        for i in enumerate(props.collections):
            if i[1].object == bpy.context.object:
                if i[1].collection != None:
                    ob_name_col_1 = i[1].collection.name
                    #changes iterateNew to 
                    iterateNew = True
                    break
                    
        #How many objects you have selected
        selected_objects = len(bpy.context.selected_objects)
        
        #Changes the text from "Object" to "Objects" if more than one object is selected
        object_text = "Object" if selected_objects <= 1 else "Objects"
        
        #Changes text from "Iterate" to "Iterate New" if object wasn't found in Backup Objects
        ob_name_iterate = "Backup %d New %s" % (selected_objects, object_text) if iterateNew == False else "Backup %d %s" % (selected_objects, object_text)
        
        #row = col.row(align=True)
        
        #row = col.row(align=True)
        #row.operator("rig_prop_man.duplicating_ops", icon="DUPLICATE", text=ob_name_iterate).type = "DUPLICATE"
        
        row = col.row(align=True)
        
        #row.label(text="Collection: "+ob_name_col_1, icon="GROUP")
        row.label(text="Collection: ", icon="GROUP")
        row.label(text=ob_name_col_1)
        
        #if props.dropdown_1 == True:
        row = col.row(align=True)
        
        row.label(text="Object: ", icon="OUTLINER_OB_MESH")
        row.label(text=ob_name_1)
            
        #Duplicate Button BOTTOM
        
        row = col.row(align=True)
        
        #This is how many collections have both an Object or Collection assigned to them
        working_collections = 0
        for i in props.collections:
            if i.collection != None and i.object != None:
                working_collections += 1
                
        row.label(text="Backup Objects (%d/%d):" % (working_collections, len(props.collections)) )
        
        #TOP
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("RIG_PROP_MAN_UL_items", "custom_def_list", props, "collections", props, "RPMN_ULIndex", rows=3)
        
        #Side_Bar Operators
        col = split.column(align=True)
        
        button = col.operator("rig_prop_man.ui_ops_move", text="", icon="TRIA_UP")
        button.type = "UP"
        
        button = col.operator("rig_prop_man.ui_ops_move", text="", icon="TRIA_DOWN")
        button.type = "DOWN"
        
        button = col.operator("rig_prop_man.ui_ops_move", text="", icon="PANEL_CLOSE")
        button.type = "REMOVE"
        
        #button = col.operator("rig_prop_man.ui_ops_select", text="", icon="RESTRICT_SELECT_OFF")
        #button.type = "SELECT_ACTIVE_UI"
        #End of CustomPanel
        

#This is a subpanel
class RIG_PROP_MAN_PT_display_settings(bpy.types.Panel):
    bl_label = "Display Settings"
    bl_parent_id = "RIG_PROP_MAN_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    def draw(self, context):
        layout = self.layout
        
        data = bpy.data
        scene = context.scene
        props = scene.RPMR_Props
        
        #collection_active: 
        #collections:
        
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Bruh Momenta")
        
#This is a subpanel
class RIG_PROP_MAN_PT_backup_settings(bpy.types.Panel):
    bl_label = "Backup Settings"
    bl_parent_id = "RIG_PROP_MAN_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        #collection_active: 
        #collections:
        
        col = layout.column()
        
        #row = col.row(align=True)
        #row.label(text="Only Active Object")
        
        row = col.row(align=True)
        row.prop(scene.RPMR_Props, "only_active", expand=True)
        
        col.separator()
        
        row = col.row(align=True)
        row.label(text="In Weight Paint")
        
        
        
class RIG_PROP_MAN_PT_cleaning(bpy.types.Panel):
    bl_label = "Cleaning Operators"
    bl_parent_id = "RIG_PROP_MAN_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        col = layout.column(align=False)
        
        row = col.row(align=True)
        row.label(text="Cleaning OOOF")
        
        #col.separator()
        
class RIG_PROP_MAN_PT_debug_panel(bpy.types.Panel):
    bl_label = "Debugging Operators"
    bl_parent_id = "RIG_PROP_MAN_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
        
        #return props.collection_parent is not None and props.collection_active is not None
        return props.debug_mode == True
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        col = layout.column(align=False)
        
        row = col.row(align=True)
        row.label(text="Print")
        
        row = col.row(align=True)
        row.operator("rig_prop_man.debug", text="Print Different").type = "PRINT_DIFFERENT_1"
        
        row = col.row(align=True)
        row.operator("rig_prop_man.debug", text="Print Objects/Collections").type = "PRINT_1"
        
        #row = col.row(align=True)
        #row.operator("rig_prop_man.debug", text="Delete Test").type = "CLEAN"
        
        #col.separator()
        
        row = col.row(align=True)
        row.label(text="Add")
        
        row = col.row(align=True)
        row.operator("rig_prop_man.debug", text="Add 3 Objects").type = "TESTING"
        
        #col.separator()
        
        row = col.row(align=True)
        
        row.label(text="Delete")
        
        row = col.row(align=True)
        #button = row.operator("rig_prop_man.debug", text="Delete All")
        #button.type = "REMOVE_UI_ALL"
        row.operator("rig_prop_man.ui_ops_move", icon="TRASH", text="All UI Elements").type = "REMOVE_UI_ALL"
            
    
class RIG_PROP_MAN_preferences(bpy.types.AddonPreferences):
    #bl_idname = "iterate_objects_addon_b2_80_v1_0"
    bl_idname = __name__
    # here you define the addons customizable props
    ui_tab: bpy.props.EnumProperty(name="Enum", items= [("GENERAL", "General", "General Options"), ("ABOUT", "About", "About Author & Where to Support")], description="Backup Object UI Tabs", default="GENERAL")
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.RPMR_Props
        
        col = layout.column()
        
        row = col.row(align=True)
        row.prop(self, "ui_tab", expand=True)
        row = col.row(align=True)
        
        box = layout.box()
        col = box.column()
        
        if self.ui_tab == "GENERAL":
            row = col.row(align=True)
            #row.label(text="Add Button to 3D Viewport Header?")
            row.prop(props, "debug_mode", expand=True, text="Debug Mode")
            
            row = col.row(align=True)
            
        elif self.ui_tab == "ABOUT":
            row = col.row(align=True)
            row.label(text="JohnGDDR5 on: ")
            row.operator("wm.url_open", text="Youtube").url = "https://www.youtube.com/channel/UCzPZvV24AXpOBEQWK4HWXIA"
            row.operator("wm.url_open", text="Twitter").url = "https://twitter.com/JohnGDDR5"
            row.operator("wm.url_open", text="Artstation").url = "https://www.artstation.com/johngddr5"

class RIG_PROP_MAN_collection_objects(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")
    collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    
    #duplicates: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    
    recent: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    custom: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    icon: bpy.props.StringProperty(name="Icon name for object", description="Used to display in the list", default="QUESTION")#, get=)#, update=checkIcon)
    
class RIG_PROP_MAN_props(bpy.types.PropertyGroup):
    #Tries to set collection_parent's default to Master Collection
    
    collection_active: bpy.props.PointerProperty(name="Collection to add Collections for Object duplicates", type=bpy.types.Collection)
    #Booleans for locking default collection of parent
    
    lock_active: bpy.props.BoolProperty(name="Lock Collection of Active", description="When locked, you can now edit the name of the selected collection", default=False)
    
    collections: bpy.props.CollectionProperty(type=RIG_PROP_MAN_collection_objects)
    
    RPMN_ULIndex: bpy.props.IntProperty(name="List Index", description="UI List Index", default= 0, min=0)
    
    clean_leave: bpy.props.IntProperty(name="List Index", description="Ammount of recent Objects to leave when cleaning.", default=2, min=0)
    
    #Dropdown for Iterate Display
    dropdown_1: bpy.props.BoolProperty(name="Dropdown", description="Show Object of Backup Object", default=False)
    
    #group_name_use: bpy.props.BoolProperty(name="Use Object Name for New Collection", description="Use the Object\'s name for the New Collection when creating a new Iteration Object", default=True)
    
    group_name: bpy.props.StringProperty(name="New Collection Name", description="Name used when creating a new collection for Active", default="Group")
    
    listDesc =  ["Displays List in order of how many duplicates each object has", "Displays List in the order they were created", "Displays List in order user specified"]
    listDesc2 =  ["List displays in Descending Order", "List displays in Ascending Order"]
    
    ##NEW CRAP
    custom_prop_placement: bpy.props.EnumProperty(name="Custom Property Placement"
        , items= [("OBJECT", "Object", listDesc[0], "OBJECT_DATA", 0), ("DATA", "Data", listDesc[1], "MESH_DATA", 1)]
        , description="Where to calculate and send Custom Properties from Addon", default="DATA")
    
    
    
    display_collections: bpy.props.BoolProperty(name="Display Collections in List", description="Backup Object Collections where duplicates are sent.", default=True)
    
    display_icons: bpy.props.BoolProperty(name="Display Icons", description="Display icons of objects in the list", default=True)
    
    display_index: bpy.props.BoolProperty(name="Display Index", description="Display index of list row", default=True)
    
    display_object_count: bpy.props.BoolProperty(name="Display Backup Object Count", description="Display amount of backed up objects in Backup Collection", default=True)
    
    index_to_new: bpy.props.BoolProperty(name="Updates Active List Row", description="Sets Active list row to newest backup object that was added.", default=True)
    
    debug_mode: bpy.props.BoolProperty(name="Enable Debug Operators", description="Enables a panel with Debugging operators for developers", default=True)
    
    debug_mode_arrow: bpy.props.BoolProperty(name="Debug Mode Dropdown Arrow", description="To display Debug Mode", default=True)
    
    #For Iterate Collection Settings and Operators
    
    error_object: bpy.props.StringProperty(name="Collection Not Found", description="Collection has been deleted or doesn\'t exist", default="[No Object]", options={'HIDDEN'})
    
    error_collection: bpy.props.StringProperty(name="Collection Not Found", description="Collection has been deleted or doesn\'t exist", default="[No Collection]", options={'HIDDEN'})
    
    #backup settings
    only_active: bpy.props.BoolProperty(name="Backup Only Active Object", description="Only the active object will be backed up", default=False)
    
    
    #END
    
    
#Classes that are registered
classes = (
    RIG_PROP_MAN_OT_select_collection,
    RIG_PROP_MAN_OT_group_operators,
    #RIG_PROP_MAN_OT_duplicate,
    #RIG_PROP_MAN_OT_cleaning,
    #RIG_PROP_MAN_OT_removing,
    
    RIG_PROP_MAN_OT_debugging,
    RIG_PROP_MAN_OT_ui_operators_move,
    #RIG_PROP_MAN_OT_ui_operators_select,
    
    RIG_PROP_MAN_UL_items,
    #RIG_PROP_MAN_MT_menu_select_collection,
    
    RIG_PROP_MAN_PT_custom_panel1,
    RIG_PROP_MAN_PT_display_settings,
    RIG_PROP_MAN_PT_backup_settings,
    RIG_PROP_MAN_PT_cleaning,
    RIG_PROP_MAN_PT_debug_panel,
    
    RIG_PROP_MAN_preferences,
    RIG_PROP_MAN_collection_objects,
    RIG_PROP_MAN_props,
)



def register():
    #ut = bpy.utils
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    #bpy.types.Scene.IM_Collections = bpy.props.CollectionProperty(type=REF_IMAGEAID_Collections)
    bpy.types.Scene.RPMR_Props = bpy.props.PointerProperty(type=RIG_PROP_MAN_props)
    
def unregister():
    #ut = bpy.utils
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.RPMR_Props
    
if __name__ == "__main__":
    register()
    

