
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

##General UI Functions & Operators - TOP
    
class customMethods:
    #def setAttributes(self, object, dictionary):
    
    #This is for being able to set multiple attributes of operators in a single line, with a dictionary. In order to reduce the lines used/repeated
    @staticmethod
    def setAttributes(object, dictionary):
        #dictionary should be attribute name and what to set its value
        #dictionary = {"type": "ADD", }
        for i in dictionary:
            if hasattr(object, i):
                setattr(object, i, dictionary[i])
                
        return None
        

#For general UI functions used for UI classes
class UI_Functions:
    
    #Copies properties from one object to another. If Duplicate Object is missing properties, it will ignore it.
    @staticmethod
    def copyAttributes(object, object_duplicate):
        attributes = []
        internal_use_ignore = []
        ignore = ('bl_rna', 'rna_type')
        missing = []
        #For loop to only get the attributes I made, not the default python and blender ones
        for i in dir(object):
            if i.startswith('__') == False and (i not in ignore):
                attributes.append(i)
            else:
                internal_use_ignore.append(i)
                
        print("internal_use_ignore: %s" % (str(internal_use_ignore) ) )
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
        
    
    @staticmethod
    def UI_Functions(collection, UI_Index, type):
        #collection is for ex. props.strings
        #UI_Index is the index of active UI list element
        
        #gets the last index of list
        list_length = len(collection)-1
        #print("UI_Index[1]: %d" % (UI_Index) )
        #Add new item to collection
        if type == "ADD":
            collection.add()
            UI_Index = len(collection)-1
            #if len(collection)
        #Basically Deletes
        elif type == "REMOVE":
            collection.remove(UI_Index)
            if UI_Index >= list_length:
                UI_Index -= 1
        #Moves up
        elif type == "UP":
            if UI_Index != 0:
                collection.move(UI_Index, UI_Index-1)
                UI_Index -= 1
            else:
                collection.move(UI_Index, list_length)
                UI_Index = list_length
        #Moves down
        elif type == "DOWN":
            if UI_Index != list_length:
                collection.move(UI_Index, UI_Index+1)
                UI_Index += 1
            else:
                collection.move(UI_Index, 0)
                UI_Index = 0
        #Creates a Duplicate of the object in the collectionlection
        elif type == "DUPLICATE":
            if list_length >= 0:
                duplicate = collection.add()
                UI_Functions.copyAttributes(collection[UI_Index], duplicate)
        #Uses the dictionary function .clear() to remove all stuff in the collection
        elif type == "CLEAR":
            collection.clear()
            UI_Index = 0
                
            
        print("UI_Functions: { type: %s, UI_Index: %d }" % (type, UI_Index) )
        return int(UI_Index)

class RIG_PROP_MAN_OT_general_ui_ops(bpy.types.Operator, customMethods):
    bl_idname = "rig_prop_man.general_ui_ops"
    bl_label = "General UI List Operators/Functions"
    bl_description = "For adding, removing and moving up/down list elements"
    bl_options = {'UNDO', 'REGISTER'}
    type: bpy.props.StringProperty(default="DEFAULT")
    collection: bpy.props.StringProperty(default="DEFAULT")
    list_index: bpy.props.StringProperty(default="DEFAULT")
    #include: bpy.props.BoolProperty(default=False)
    #mirror: bpy.props.BoolProperty(default=False)
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    @classmethod
    def setAttributes(cls, dictionary):
        #dictionary should be attribute name and what to set its value
        #dictionary = {"type": "ADD", }
        for i in dictionary:
            if hasattr(cls, i):
                setattr(cls, i, dictionary[i])
                
        return None
    
    
    #Resets default settings
    #@classmethod
    @staticmethod
    def resetSelf(self):
        self.type = "DEFAULT"
        self.collection = "DEFAULT"
        self.list_index = "DEFAULT"
        print("Reset States: %s, %s, %s" % (self.type, self.collection, self.list_index) )
    
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
                new_UI_Index = UI_Functions.UI_Functions(collection, UI_Index, self.type)
                setattr(props, self.list_index, new_UI_Index )
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

class RIG_PROP_MAN_OT_copy_paste_prop(bpy.types.Operator):
    bl_idname = "rig_prop_man.copy_paste_prop"
    bl_label = "Copy/Paste a selected Custom Property"
    bl_description = "Copies and Paste from a selected Custom Property"
    bl_options = {'UNDO',}

    name: bpy.props.StringProperty(default="[DEFAULT VALUE]")
    prefix: bpy.props.StringProperty(default="")
    value: bpy.props.StringProperty(default="")
    default: bpy.props.StringProperty(default="")
    min: bpy.props.FloatProperty(default= -10000)
    max: bpy.props.FloatProperty(default= 10000)
    soft_min: bpy.props.FloatProperty(default= -10000)
    soft_max: bpy.props.FloatProperty(default= 10000)
    description: bpy.props.StringProperty(default="")
    use_soft_limits: bpy.props.BoolProperty(default=False)

    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=-1)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props

        attributes = [
            "name", 
            "prefix", 
            "value", 
            "default",
            "min",
            "max",
            "soft_min",
            "soft_max",
            "description",
            "use_soft_limits",
            ]
            
        if self.type == "COPY":
            reportString = "Copied Property"
            
            if len(props.collection_properties) > 0:
                active_index = props.ULIndex_Properties
                active_prop = props.collection_properties[active_index]
                
                for j in attributes:
                    setattr(self, j, getattr(active_prop, j) )
            else:
                reportString = "No Properties to Copy from"
        elif self.type == "PASTE":
            #This is to prevent pasting all the default values, which is unwanted
            if self.name != "[DEFAULT VALUE]":
                reportString = "Pasted Property"
                
                if len(props.collection_properties) > 0:
                    active_index = props.ULIndex_Properties
                    active_prop = props.collection_properties[active_index]
                    
                    for j in attributes:
                        setattr(active_prop, j, getattr(self, j) )
                else:
                    reportString = "No Properties to Paste to"
            else:
                reportString = "No Properties copied from"
        else:
            reportString = "Operator Type Unset"

        self.report({'INFO'}, reportString)
            
        self.type == "DEFAULT"
        
        return {'FINISHED'}

class RIG_PROP_MAN_OT_generate_custom_props(bpy.types.Operator):
    bl_idname = "rig_prop_man.generate_custom_props"
    bl_label = "Create a new Collection"
    bl_description = "Generates Custom Properties where specified by the user. Can also replace existing Custom Properties if allowed to by the User in Addon Prerefences"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=0)
    
    count_new = 0
    count_updated = 0
    
    @classmethod
    def getCount(cls):
        return [cls.count_new, cls.count_updated]
        
    @classmethod
    def setCount(cls, count_new=None, count_updated=None):
        #cls.count_new = count_new if count_new != None else pass
        #cls.count_updated = count_updated if count_updated != None else pass
        if count_new != None:
            cls.count_new = count_new 
        if count_updated != None:
            cls.count_updated = count_updated
        return None
    
    @classmethod
    def addCount(cls, count_new=None, count_updated=None):
        #cls.count_new = count_new if count_new != None else pass
        #cls.count_updated = count_updated if count_updated != None else pass
        if count_new != None:
            cls.count_new += count_new 
        if count_updated != None:
            cls.count_updated += count_updated
        return None
        
    @classmethod
    def resetCount(cls):
        cls.count_new = 0
        cls.count_updated = 0
        return None
    
    #list("[0 , 0, 0]".strip("[] ").replace(" ", "").split(","))
    def checkIfList(self, string):
        #removes "\"" and "[" and "]", then splits from "," to a list
        string_list = string.strip("[] ").replace(" ", "").replace("\"", "").split(",")
        print(string_list)
        for i in enumerate(string_list):
            #integer
            try:
                string_list[i[0]] = int(string_list[i[0]])
                continue
            except:
                pass
            #float
            try:
                string_list[i[0]] = float(string_list[i[0]])
                continue
            except:
                pass
            #string
            try:
                string_list[i[0]] = str(string_list[i[0]])
                continue
            except:
                pass
                
        type_previous = string_list[0].__class__.__name__
        compatible_types = ["int", "float"]
        is_convertible = True
        
        #excludes 1st index
        for i in string_list[1:]:
            index_type = i.__class__.__name__
            if index_type == type_previous or index_type in compatible_types:
                continue
            else:
                is_convertible = False
                break
        print(string_list)
        
        #If types are either (int or float) or just (string), not all 3
        if is_convertible == True:
            #string
            try:
                string_list = list(string_list)
                return string_list
            except:
                return None
        else:
            return None
    
    def valueConvert(self, string):
        value = string
        #int
        try:
            value = int(string)
            return value
        except:
            #pass
            #float
            try:
                value = float(string)
                return value
            except:
                pass
            #dictionary
            try:
                value = dict(string)
                return value
            except:
                pass
            #list
            try:
                #value = list(string)
                value = self.checkIfList(string)
                return value
            except:
                pass
        return value
        
    def evalSafety(self, string):
        #bpy.context.object.data.bones.active.bl_rna.__module__
        #Returns 'bpy_types' or 'bpy.types'
        should_have = ["bpy_types", "bl.types"]
        try:
            object = eval(string)
        except:
            object = None
        
        if hasattr(object, "bl_rna") == True:
            if getattr(object.bl_rna, "__module__") in should_have:
                print("Successful evaluation of path: \" %s \"" % (string) )
                pass
            else:
                object = None
                print("path \" %s \" isn\"t or already in \"__module__\" from \"bpy_types\" " % (string) )
        else:
            print("path \" %s \" can't be evaluated or already in \"bl_rna\" from \"bpy_types\" " % (string) )
            
        return object
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RPMR_Props
        
        reportString = "Done"
        print("OOF: -1")
        
        attributes = [
            "default",
            "min",
            "max",
            "soft_min",
            "soft_max",
            "description",
            "use_soft_limits",
            ]
        
        if len(props.collection_strings) > 0:
            """
            active_index = props.ULIndex_Strings
            active_string = props.collection_strings[active_index]
            """
            #Where to create the Custom Properties
            if props.custom_prop_placement == "OBJECT":
                placement = context.object
            elif props.custom_prop_placement == "DATA":
                placement = context.object.data
            elif props.custom_prop_placement == "SCENE":
                placement = context.scene
            elif props.custom_prop_placement == "WORLD":
                placement = context.scene.world
            else:
                #placement = props.custom_path
                placement = self.evalSafety(props.custom_path)
                
                
            if placement != None:
                
                #if self.type == "DEFAULT":
                active_index = props.ULIndex_Strings
                active_string = props.collection_strings[active_index]
                    
                #for h in enumerate():
                
                print("OOF: 2")
                print(active_string.__class__)
                print(active_string.__class__.__name__)
                count_new = 0
                count_updated = 0
                
                def generateProperties(collection_properties, active_string):
                    count_new = 0
                    count_updated = 0
                    
                    #goes through every custom Property to generate
                    #for i in enumerate(props.collection_properties):
                    for i in enumerate(collection_properties):
                    
                        if i[1].use == True:
                            #bpy.context.object["_RNA_UI"] = {"Bruh0": {"min": -1.5, "max": 1.5, "soft_min": 0.5, "use_soft_limits": True} }
                            name_with_prefix = str(i[1].prefix) + active_string.name
                            
                            if name_with_prefix not in placement:
                                placement[name_with_prefix] = self.valueConvert(i[1].value)
                                
                                count_new += 1
                            else:
                                if props.replace_existing_props == True:
                                    placement[name_with_prefix] = self.valueConvert(i[1].value)
                                    
                                print("Attribute Exists: %s" % (name_with_prefix) )
                                count_updated += 1
                                
                            if placement[name_with_prefix].__class__.__name__ != 'IDPropertyGroup':
                                new_dict = {name_with_prefix: {} }
                                
                                #This is where all the generated attributes are placed to be created with "_RNA_UI"
                                for j in attributes:
                                    new_dict[name_with_prefix][j] = getattr(i[1], j)
                                    
                                placement["_RNA_UI"] = new_dict
                            else:
                                print("Was a dictionary: %s" % (name_with_prefix) )
                                pass
                    return [count_new, count_updated]
                    
                if self.type == "DEFAULT":
                    count_list_final = generateProperties(props.collection_properties, active_string)
                else:
                    count_list_final = [0, 0]
                    
                    for i in enumerate(props.collection_strings):
                        active_string = props.collection_strings[i[0]]
                        
                        #asssigned a list from generateProperties()
                        count_list = generateProperties(props.collection_properties, active_string)
                        
                        #count_list_final[0] += count_list[0]
                        #count_list_final[1] += count_list[1]
                        self.addCount(count_list[0], count_list[1])
                        
                #count_new = count_list_final[0]
                #count_updated = count_list_final[1]
                        
                        
                #Clears all the values, so it stays like before
                #placement["_RNA_UI"].clear()
                #reportString = "Custom Props: Added New: %d; Updated Existing: %d" % (count_new, count_updated)
                reportString = "Custom Props: Added New: %d; Updated Existing: %d" % (self.count_new, self.count_updated)
                
                self.resetCount()
                
            #Just error statements
            else:
                if props.custom_prop_placement == "OBJECT":
                    reportString = "No Object selected"
                elif props.custom_prop_placement == "DATA":
                    reportString = "No Object selected"
                elif props.custom_prop_placement == "SCENE":
                    reportString = "No Scene Found"
                elif props.custom_prop_placement == "WORLD":
                    reportString = "No World Found"
                else:
                    reportString = "Couldn\'t evaluate custom path. Check Console."
        else:
            reportString = "No Active Property Object"
            
        self.report({'INFO'}, reportString)
        
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
##Operator Template
"""
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
        active = props.ULIndex_Strings
        
            
        
        #Resets self props into "DEFAULT"
        self.type == "DEFAULT"
        self.sub == "DEFAULT"
        
        return {'FINISHED'}
"""

#List drawing Class
class RIG_PROP_MAN_UL_items_strings(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        #active = props.RIA_ULIndex
        RPMR_Collection = props.collection_strings
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(RPMR_Collection) > 0:
                row.prop(item, "name", text="", emboss=False)
                
            else:
                row.label(text="No Iterations Here")
                
        #Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass
        
#List drawing Class
class RIG_PROP_MAN_UL_items_properties(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        #active = props.RIA_ULIndex
        RPMR_Collection = props.collection_strings
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(RPMR_Collection) > 0:
                row.prop(item, "use", text="", emboss=True)
                row.prop(item, "name", text="", emboss=False)
                
            else:
                row.label(text="No Iterations Here")
                
        #Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass

class RIG_PROP_MAN_MT_dropdown_menu_ui_generate(bpy.types.Menu):
    bl_idname = "RIG_PROP_MAN_MT_dropdown_menu_ui_generate"
    bl_label = "Extra UI Functions & Operators"
    bl_description = "Extra functions for generating Custom Properties"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        col = layout.column()
        
        #row = col.row(align=True)
        button = col.operator("rig_prop_man.generate_custom_props", icon="ADD", text="For All String Names")
        button.type = "ALL"
        

class RIG_PROP_MAN_MT_dropdown_menu_ui_properties(bpy.types.Menu):
    bl_idname = "RIG_PROP_MAN_MT_dropdown_menu_ui_properties"
    bl_label = "Extra UI Functions & Operators"
    bl_description = "Copy/Paste and Duplicate functions"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RPMR_Props
        
        col = layout.column()
        
        #row = col.row(align=True)
        
        properties = {"collection": "collection_properties", "list_index": "ULIndex_Properties"}
        
        #Copy/Paste
        button = col.operator("rig_prop_man.copy_paste_prop", text="Copy", icon="COPYDOWN")
        button.type = "COPY"
        
        button = col.operator("rig_prop_man.copy_paste_prop", text="Paste", icon="PASTEDOWN")
        button.type = "PASTE"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="Duplicate", icon="DUPLICATE")
        self.setAttributes(button, properties)
        button.type = "DUPLICATE"

class RIG_PROP_MAN_PT_custom_panel1(bpy.types.Panel, customMethods):
    #A Custom Panel in Viewport
    bl_idname = "RIG_PROP_MAN_PT_custom_panel1"
    bl_label = "Property Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Prop Man"
    
    #collectionOOF: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    
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
        row.prop(props, "custom_prop_placement", text="", expand=False)
        
        if props.custom_prop_placement == "CUSTOM":
            row = col.row(align=True)
            row.prop(props, "custom_path", expand=True, text="Path")
        
        col.separator()
        
        row = col.row(align=True)
        row.label(text="Generate Properties:")
        
        row = col.row(align=True)
            
        row.operator("rig_prop_man.generate_custom_props", icon="ADD", text="For Active String Name")
        #Copy/Paste Menu
        row.menu("RIG_PROP_MAN_MT_dropdown_menu_ui_generate", icon="DOWNARROW_HLT", text="")
        
        #Separates for extra space between
        col.separator()
            
        #Duplicate Button BOTTOM
        
        row = col.row(align=True)
        row.label(text="Property Strings Names: %d" % (len(props.collection_strings) ) )
        
        #row = col.row(align=True)
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("RIG_PROP_MAN_UL_items_strings", "custom_def_list", props, "collection_strings", props, "ULIndex_Strings", rows=3)
        
        #Side_Bar Operators
        col = split.column(align=True)
        
        properties = {"collection": "collection_strings", "list_index": "ULIndex_Strings"}
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="ADD")
        self.setAttributes(button, properties)
        button.type = "ADD"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="TRIA_UP")
        self.setAttributes(button, properties)
        button.type = "UP"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="TRIA_DOWN")
        self.setAttributes(button, properties)
        button.type = "DOWN"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="PANEL_CLOSE")
        self.setAttributes(button, properties)
        button.type = "REMOVE"
        
        
        
        col = layout.column()
        
        
        col.separator()
            
        #Duplicate Button BOTTOM
        
        row = col.row(align=True)
        row.label(text="Properties: %s" % (len(props.collection_properties) ))
        
        #row = col.row(align=True)
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("RIG_PROP_MAN_UL_items_properties", "custom_def_list", props, "collection_properties", props, "ULIndex_Properties", rows=3)
        
        #Side_Bar Operators
        col = split.column(align=True)
        
        properties = {"collection": "collection_properties", "list_index": "ULIndex_Properties"}
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="ADD")
        self.setAttributes(button, properties)
        button.type = "ADD"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="TRIA_UP")
        self.setAttributes(button, properties)
        button.type = "UP"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="TRIA_DOWN")
        self.setAttributes(button, properties)
        button.type = "DOWN"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="PANEL_CLOSE")
        self.setAttributes(button, properties)
        button.type = "REMOVE"
        
        #Copy/Paste Menu
        col.menu("RIG_PROP_MAN_MT_dropdown_menu_ui_properties", icon="DOWNARROW_HLT", text="")
        
        """
        #Copy/Paste
        button = col.operator("rig_prop_man.copy_paste_prop", text="", icon="COPYDOWN")
        button.type = "COPY"
        
        button = col.operator("rig_prop_man.copy_paste_prop", text="", icon="PASTEDOWN")
        button.type = "PASTE"
        
        button = col.operator("rig_prop_man.general_ui_ops", text="", icon="DUPLICATE")
        self.setAttributes(button, properties)
        button.type = "DUPLICATE"
        """
        
        #End of CustomPanel
        

#This is a subpanel
class RIG_PROP_MAN_PT_property(bpy.types.Panel, customMethods):
    bl_label = "Property"
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
        
        active_index = props.ULIndex_Properties
        
        col = layout.column()
        
        if len(props.collection_properties) > 0:
            
            row = col.row(align=True)
            row.label(text="Bruh Momenta")
            
            
            active_prop = props.collection_properties[active_index]
            
            row = col.row(align=True)
            row.prop(active_prop, "prefix", text="Prefix")
            
            row = col.row(align=True)
            row.prop(active_prop, "value", text="Value")
            
            row = col.row(align=True)
            row.prop(active_prop, "default", text="Default")
            
            row = col.row(align=True)
            row.prop(active_prop, "min", text="Min")
            row.prop(active_prop, "max", text="Max")
            
            row = col.row(align=True)
            row.prop(active_prop, "soft_min", text="Soft Min", expand=False, emboss=True)
            row.prop(active_prop, "soft_max", text="Soft Max")
            
            row = col.row(align=True)
            row.prop(active_prop, "use_soft_limits", text="Use Soft Limits")
            
            row = col.row(align=True)
            row.prop(active_prop, "description", text="Description")
            
            
        else:
            row = col.row(align=True)
            
            properties = {"collection": "collection_properties", "list_index": "ULIndex_Properties"}
            
            button = col.operator("rig_prop_man.general_ui_ops", text="Add Properties to edit", icon="ADD")
            self.setAttributes(button, properties)
            button.type = "ADD"
            #row.label(text="Add Properties to edit")
            #row.enabled = False
            


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
            row.prop(props, "replace_existing_props", expand=True, text="Replace/Update Existng Properties")
            
            row = col.row(align=True)
            
        elif self.ui_tab == "ABOUT":
            row = col.row(align=True)
            row.label(text="JohnGDDR5 on: ")
            row.operator("wm.url_open", text="Youtube").url = "https://www.youtube.com/channel/UCzPZvV24AXpOBEQWK4HWXIA"
            row.operator("wm.url_open", text="Twitter").url = "https://twitter.com/JohnGDDR5"
            row.operator("wm.url_open", text="Artstation").url = "https://www.artstation.com/johngddr5"

#options for a single property
class RIG_PROP_MAN_property:
    prefix: bpy.props.StringProperty(name="Prefix", default="")
    value: bpy.props.StringProperty(name="Value", default="")
    default: bpy.props.StringProperty(name="Default Value", default="")
    min: bpy.props.FloatProperty(name="Min", description="Min", default= -10000)#, min=0)
    max: bpy.props.FloatProperty(name="Max", description="Max", default= 10000)#, min=0)
    soft_min: bpy.props.FloatProperty(name="Soft Min", description="Soft Min", default= -10000)#, min=0)
    soft_max: bpy.props.FloatProperty(name="Soft Max", description="Soft Max", default= 10000)#, min=0)
    description: bpy.props.StringProperty(name="Description", description="Description of Custom Property", default="")
    use_soft_limits: bpy.props.BoolProperty(name="Use Soft Limits", description="Use Soft Limits", default=False)
    

class RIG_PROP_MAN_properties(bpy.types.PropertyGroup, RIG_PROP_MAN_property):
    name: bpy.props.StringProperty(name="Property Description Note", default="[Property Note]"
    , description="Name of Property that will be mirrored and generated with Prefixes. Useful for repeating Custom Property names. Ex. armature bones \"Leg.Back.L\" ")
    #property: bpy.props.CollectionProperty(name="Added Collections to List", type=RIG_PROP_MAN_property)
    
    use: bpy.props.BoolProperty(name="Create this property for the Property Name", description="", default=True)

class RIG_PROP_MAN_property_strings(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property Name", default="[Property Name]"
    , description="Name of Property that will be mirrored and generated with Prefixes. Useful for repeating Custom Property names. Ex. armature bones \"Leg.Back.L\" ")
    #collection: bpy.props.CollectionProperty(name="Added Collections to List", type=RIG_PROP_MAN_property_string_booleans)
    
    #collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    #object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    
##THIS ONE ISNT USED
class RIG_PROP_MAN_collection_objects(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property Name", default="")
    prefix: bpy.props.StringProperty(name="Prefix", default="")
    collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    
    #duplicates: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    
    recent: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    custom: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    icon: bpy.props.StringProperty(name="Icon name for object", description="Used to display in the list", default="QUESTION")#, get=)#, update=checkIcon)
    
class RIG_PROP_MAN_props(bpy.types.PropertyGroup):
    #Tries to set collection_parent's default to Master Collection
    
    collections: bpy.props.CollectionProperty(type=RIG_PROP_MAN_collection_objects)
    
    collection_strings: bpy.props.CollectionProperty(type=RIG_PROP_MAN_property_strings)
    collection_properties: bpy.props.CollectionProperty(type=RIG_PROP_MAN_properties)
    
    #Index for Strings_Collection
    ULIndex_Strings: bpy.props.IntProperty(name="String List Index", description="Active UI String List Index", default= 0, min=0)
    
    #Index for Properties Collection
    ULIndex_Properties: bpy.props.IntProperty(name="Properties List Index", description="Active UI Properties List Index", default= 0, min=0)
    
    #Dropdown for Iterate Display
    replace_existing_props: bpy.props.BoolProperty(name="Replace Existing Custom Properties", description="Replace existing properties with the same name with the new updated values.", default=True)
    
    repeating = "Places generated Custom Properites in "
    
    listDesc =  [
    repeating + "Object",
    repeating + "Object's Data",
    repeating + "Scene Data",
    repeating + "Scene Data",
    repeating + "World Data",
    repeating + "Custom Data Path. ex. \"bpy.context.object\""
    ]
    
    ##NEW CRAP
    custom_prop_placement: bpy.props.EnumProperty(name="Custom Property Placement"
        , items= [
        ("OBJECT", "Object", listDesc[0], "OBJECT_DATA", 0),
        ("DATA", "Data", listDesc[1], "MESH_DATA", 1),
        ("SCENE", "Scene", listDesc[2], "SCENE_DATA", 2),
        ("WORLD", "World", listDesc[3], "WORLD_DATA", 3),
        ("CUSTOM", "Custom Path", listDesc[4], "FILE_TEXT", 4),
        ]
        , description="Where to calculate and send Custom Properties from Addon", default="DATA")
        
    custom_path: bpy.props.StringProperty(name="Property Name", default="bpy.context.object")
    
    
    #END
    
    
#Classes that are registered
classes = (
    #customMethods,
    RIG_PROP_MAN_OT_general_ui_ops,
    
    RIG_PROP_MAN_OT_copy_paste_prop,
    RIG_PROP_MAN_OT_generate_custom_props,
    #RIG_PROP_MAN_OT_duplicate,
    #RIG_PROP_MAN_OT_cleaning,
    #RIG_PROP_MAN_OT_removing,
    
    #RIG_PROP_MAN_OT_debugging,
    #RIG_PROP_MAN_OT_ui_operators_move,
    #RIG_PROP_MAN_OT_ui_operators_select,
    
    RIG_PROP_MAN_UL_items_strings,
    RIG_PROP_MAN_UL_items_properties,
    
    RIG_PROP_MAN_MT_dropdown_menu_ui_generate,
    RIG_PROP_MAN_MT_dropdown_menu_ui_properties,
    
    RIG_PROP_MAN_PT_custom_panel1,
    RIG_PROP_MAN_PT_property,
    #RIG_PROP_MAN_PT_backup_settings,
    #RIG_PROP_MAN_PT_cleaning,
    #RIG_PROP_MAN_PT_debug_panel,
    
    RIG_PROP_MAN_preferences,
    
    #RIG_PROP_MAN_property,
    RIG_PROP_MAN_properties,
    
    
    RIG_PROP_MAN_property_strings,
    
    
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
    
    print(RIG_PROP_MAN_OT_general_ui_ops.__mro__)
    
def unregister():
    #ut = bpy.utils
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.RPMR_Props
    
if __name__ == "__main__":
    register()
    

