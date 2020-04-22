

import bpy

import ast # For string to dictionary evaluations
import re # For RegEx

#Imports Blender Properties ex. BoolProperty
from bpy.props import *

# options for a single property
class PROP_BUILDER_property:
    prefix: bpy.props.StringProperty(name="Prefix", default="", description="Added before Property Name")
    value: bpy.props.StringProperty(name="Value", default="1.0")
    default: bpy.props.StringProperty(name="Default Value", default="1.0")
    min: bpy.props.FloatProperty(name="Min", description="Min", default= 0)# , min=0)
    max: bpy.props.FloatProperty(name="Max", description="Max", default= 1)# , min=0)
    soft_min: bpy.props.FloatProperty(name="Soft Min", description="Soft Min", default= 0)# , min=0)
    soft_max: bpy.props.FloatProperty(name="Soft Max", description="Soft Max", default= 1)# , min=0)
    description: bpy.props.StringProperty(name="Description", description="Description of Custom Property", default="")
    use_soft_limits: bpy.props.BoolProperty(name="Use Soft Limits", description="Use Soft Limits", default=False)
    

class PROP_BUILDER_properties(bpy.types.PropertyGroup, PROP_BUILDER_property):
    name: bpy.props.StringProperty(name="Property Description Note", default="[Property Note]"
    , description="Name of Property that will be mirrored and generated with Prefixes. Useful for repeating Custom Property names. Ex. armature bones \"Leg.Back.L\" ")
    # property: bpy.props.CollectionProperty(name="Added Collections to List", type=PROP_BUILDER_property)
    
    use: bpy.props.BoolProperty(name="Create this property for the Property Name", description="", default=True)

class PROP_BUILDER_property_names(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property Name", default="[Property Name]"
    , description="Name of Property that will be mirrored and generated with Prefixes. Useful for repeating Custom Property names. Ex. armature bones \"Leg.Back.L\" ")


class PROP_BUILDER_props(bpy.types.PropertyGroup):
    #collections for custom Property Groups
    collection_names: bpy.props.CollectionProperty(type=PROP_BUILDER_property_names)
    collection_properties: bpy.props.CollectionProperty(type=PROP_BUILDER_properties)
    
    # Index for collection_names
    ULIndex_Names: bpy.props.IntProperty(name="String List Index", description="Active UI String List Index", default= 0, min=0)
    
    # Index for collection_properties
    ULIndex_Properties: bpy.props.IntProperty(name="Properties List Index", description="Active UI Properties List Index", default= 0, min=0)
    
    # Options
    replace_existing_props: bpy.props.BoolProperty(name="Replace Existing Custom Properties", description="Replace existing properties with the same name with the new updated values.", default=True)
    generate_flipped: bpy.props.BoolProperty(name="Generate Flipped L/R Properties", description="Property Names with a direction will also have a flipped equivalent be made", default=True)

    repeating = "Places generated Custom Properites in "
    
    listDesc =  [
    repeating + "Object",
    repeating + "Object's Data",
    repeating + "Scene Data",
    repeating + "Scene Data",
    repeating + "World Data",
    repeating + "Pose Bone Data",
    repeating + "Armature Bone Data",
    repeating + "Custom Data Path. ex. \"bpy.context.object\""
    ]
    
    ## Select where to place Custom Properties
    custom_prop_placement: bpy.props.EnumProperty(name="Custom Property Placement"
        , items= [
        ("OBJECT", "Object", listDesc[0], "OBJECT_DATA", 0),
        ("DATA", "Data", listDesc[1], "MESH_DATA", 1),
        ("SCENE", "Scene", listDesc[2], "SCENE_DATA", 2),
        ("WORLD", "World", listDesc[3], "WORLD_DATA", 3),
        ("POSE", "Pose Bone", listDesc[4], "ARMATURE_DATA", 4),
        ("BONE", "Armature Bone", listDesc[5], "BONE_DATA", 5),
        ("CUSTOM", "Custom Path", listDesc[6], "FILE_TEXT", 6),
        ]
        , description="Where to calculate and send Custom Properties from Addon", default="OBJECT")
        
    custom_path: bpy.props.StringProperty(name="Property Name", default="bpy.context.object")

    ## Where to Transfer Custom Properties From
    transfer_from: bpy.props.EnumProperty(name="Transfer Custom Properties From"
        , items= [
        ("OBJECT", "Object", listDesc[0], "OBJECT_DATA", 0),
        ("DATA", "Data", listDesc[1], "MESH_DATA", 1),
        ("SCENE", "Scene", listDesc[2], "SCENE_DATA", 2),
        ("WORLD", "World", listDesc[3], "WORLD_DATA", 3),
        ("POSE", "Pose Bone", listDesc[4], "ARMATURE_DATA", 4),
        ("BONE", "Armature Bone", listDesc[5], "BONE_DATA", 5),
        ("CUSTOM", "Custom Path", listDesc[6], "FILE_TEXT", 6),
        ]
        , description="Where to Duplicate Custom Properties from", default="OBJECT")

    ## Where to Transfer Custom Properties From
    transfer_to: bpy.props.EnumProperty(name="Transfer Custom Properties To"
        , items= [
        ("OBJECT", "Object", listDesc[0], "OBJECT_DATA", 0),
        ("DATA", "Data", listDesc[1], "MESH_DATA", 1),
        ("SCENE", "Scene", listDesc[2], "SCENE_DATA", 2),
        ("WORLD", "World", listDesc[3], "WORLD_DATA", 3),
        ("POSE", "Pose Bone", listDesc[4], "ARMATURE_DATA", 4),
        ("BONE", "Armature Bone", listDesc[5], "BONE_DATA", 5),
        ("CUSTOM", "Custom Path", listDesc[6], "FILE_TEXT", 6),
        ]
        , description="Where to Duplicate Custom Properties to", default="OBJECT")
    
    
    # END

## General UI Functions & Operators - TOP

class customMethods:
    # def setAttributes(self, object, dictionary):
    
    # This is for being able to set multiple attributes of operators in a single line, with a dictionary. In order to reduce the lines used/repeated
    @staticmethod
    def setAttributes(object, dictionary):
        # dictionary should be attribute name and what to set its value
        # dictionary = {"type": "ADD", }
        for i in dictionary:
            if hasattr(object, i):
                setattr(object, i, dictionary[i])
                
        return None
        

# For general UI functions used for UI classes
class UI_Functions:
    
    # Copies properties from one object to another. If Duplicate Object is missing properties, it will ignore it.
    @staticmethod
    def copyAttributes(object, object_duplicate):
        attributes = []
        internal_use_ignore = []
        ignore = ('bl_rna', 'rna_type')
        missing = []
        # For loop to only get the attributes I made, not the default python and blender ones
        for i in dir(object):
            if i.startswith('__') == False and (i not in ignore):
                attributes.append(i)
            else:
                internal_use_ignore.append(i)
                
        ##print("internal_use_ignore: %s" % (str(internal_use_ignore) ) )
        ##print("attributes: %s" % (str(attributes) ) )
        
        for i in attributes:
            if hasattr(object_duplicate, i):
                original_attr = getattr(object, i)
                setattr(object_duplicate, i, original_attr)
            else:
                missing.append(i)
        
        # Prints the missing attributes for debugging
        if len(missing) > 0:
            class_name = object_duplicate.__class__.__name__
            print("%s missing %d attributes: %s" % (class_name, len(missing), str(missing) ) )
        
    
    @staticmethod
    def UI_Functions(collection, UI_Index, type):
        # collection is for ex. props.strings
        # UI_Index is the index of active UI list element
        
        # gets the last index of list
        list_length = len(collection)-1
        # print("UI_Index[1]: %d" % (UI_Index) )
        # Add new item to collection
        if type == "ADD":
            collection.add()
            UI_Index = len(collection)-1
            # if len(collection)
        # Basically Deletes
        elif type == "REMOVE":
            collection.remove(UI_Index)
            if UI_Index >= list_length:
                UI_Index -= 1
        # Moves up
        elif type == "UP":
            if UI_Index != 0:
                collection.move(UI_Index, UI_Index-1)
                UI_Index -= 1
            else:
                collection.move(UI_Index, list_length)
                UI_Index = list_length
        # Moves down
        elif type == "DOWN":
            if UI_Index != list_length:
                collection.move(UI_Index, UI_Index+1)
                UI_Index += 1
            else:
                collection.move(UI_Index, 0)
                UI_Index = 0
        # Creates a Duplicate of the object in the collectionlection
        elif type == "DUPLICATE":
            if list_length >= 0:
                duplicate = collection.add()
                UI_Functions.copyAttributes(collection[UI_Index], duplicate)
        # Uses the dictionary function .clear() to remove all stuff in the collection
        elif type == "CLEAR":
            collection.clear()
            UI_Index = 0
                
            
        ##print("UI_Functions: { type: %s, UI_Index: %d }" % (type, UI_Index) )
        return int(UI_Index)

#Returns re.Pattern Object, precompiled
def regexPattern():
    #Pattern used for left/right
    pattern = r'(?i)(?<=[ \.\-_])[rRlL]((?=$|[ \.\-_])|(ight|eft))'

    #rawPattern = r'%s' % (pattern)
    #p = re.compile(rawPattern)
    p = re.compile(pattern)
    return p

#Requires a patternObject, so it won't have to recompile it
def flipDirection(string, patternObject):
    #Will return "l" or "r"
    #print("getDirection(): %s" % (string) )
    #p = regexPattern()
    p = patternObject

    match = p.search(string)

    if match is not None:
        #indexes of match ex. (5, 7)
        span = match.span()

        matchString = match.group(0)
        #sides = ("left", "right")
        direction = {"l": "right", "r": "left"}
        #stringNew = string
        #stringNew = matchString
        lowered = matchString[0].lower()
        wasUpper = matchString[0].isupper()
        wasSingle = (len(matchString) == 1)

        #changes the direction
        stringNew = direction[lowered]
        
        #1st letter to uppercase
        if wasUpper == True:
            stringNew = stringNew.capitalize()
        #single letter or whole word
        if wasSingle == True:
            stringNew = stringNew[0]
                
        print("getDirection(): %s, %s" % (matchString, stringNew) )

        #Replaces match section of String with the flipped one
        string = string[:span[0]] + stringNew + string[span[1]:]

        return string
    else:
        print("getDirection(): Match Fail for %s" % (string) )
        #return ""
        return None
    

class PROP_BUILDER_OT_general_ui_ops(bpy.types.Operator, customMethods):
    bl_idname = "prop_builder.general_ui_ops"
    bl_label = "General UI List Operators/Functions"
    bl_description = "For adding, removing and moving up/down list elements"
    bl_options = {'UNDO', 'REGISTER'}
    type: bpy.props.StringProperty(default="DEFAULT")
    collection: bpy.props.StringProperty(default="DEFAULT")
    list_index: bpy.props.StringProperty(default="DEFAULT")
    # include: bpy.props.BoolProperty(default=False)
    # mirror: bpy.props.BoolProperty(default=False)
    # sub: bpy.props.StringProperty(default="DEFAULT")
    # index: bpy.props.IntProperty(default=0, min=0)
    
    @classmethod
    def setAttributes(cls, dictionary):
        # dictionary should be attribute name and what to set its value
        # dictionary = {"type": "ADD", }
        for i in dictionary:
            if hasattr(cls, i):
                setattr(cls, i, dictionary[i])
                
        return None
    
    
    # Resets default settings
    # @classmethod
    @staticmethod
    def resetSelf(self):
        self.type = "DEFAULT"
        self.collection = "DEFAULT"
        self.list_index = "DEFAULT"
        print("Reset States: %s, %s, %s" % (self.type, self.collection, self.list_index) )
    
    @classmethod # This one seems useless
    def poll(cls, context):
        # return cls.collection != "DEFAULT"
        # print("cls.collection: %s" % (str(cls.collection)) )
        # return collection != "DEFAULT"
        return True
    
    # Use for later
    # Checks if object has attribute and returns it, else returns None
    # @staticmethod # Uncomment this after adding it
    def returnAttribute(self, object, attributeString):
        if hasattr(object, attributeString):
            return getattr(object, attributeString)
        else:
            return None
    
    def execute(self, context):
        scene = bpy.context.scene
        # context = bpy.context
        data = context.object.data
        props = scene.PPBR_Props
        
        reportString = "Done!"
        
        collection = self.returnAttribute(props, self.collection)
        UI_Index = self.returnAttribute(props, self.list_index)
        
        if collection != None:
            # Need != None, as "if" returns False if number is "0"
            if UI_Index != None:
                # props.RS_ULIndex_ReGex = UI_Functions(self.collection, self.list_index, self.type)
                
                # getattr(props, self.list_index) = UI_Functions(collection, UI_Index, self.type)
                new_UI_Index = UI_Functions.UI_Functions(collection, UI_Index, self.type)
                setattr(props, self.list_index, new_UI_Index )
            else:
                reportString = "List_Index given wasn't found in scene.PPBR_Props"
        else:
            reportString = "Collection given wasn't found in scene.PPBR_Props"
        # Resets default settings
        self.resetSelf(self)
        
        ##print(reportString)
        self.report({'INFO'}, reportString)
        
        return {'FINISHED'}

## General UI Functions & Operators - TOP

class PROP_BUILDER_OT_copy_paste_prop(bpy.types.Operator, PROP_BUILDER_property):
    bl_idname = "prop_builder.copy_paste_prop"
    bl_label = "Copy/Paste a selected Custom Property"
    bl_description = "Copies and Paste from a selected Custom Property"
    bl_options = {'UNDO',}

    name: bpy.props.StringProperty(default="[DEFAULT VALUE]")

    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=-1)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.PPBR_Props

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
            # This is to prevent pasting all the default values, which is unwanted
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

class PROP_BUILDER_OT_generate_custom_props(bpy.types.Operator):
    bl_idname = "prop_builder.generate_custom_props"
    bl_label = "Create a new Collection"
    bl_description = "Generates Custom Properties where specified by the user. Can also replace existing Custom Properties if allowed to by the User in Addon Prerefences"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=0)
    
    # class variables to count how many new Custom Properties were made
    count_new = 0
    count_updated = 0
    
    # Temporary Class variable where Custom Properties are set
    placement = None
    
    @classmethod
    def resetDefaults(cls):
        cls.type = "DEFAULT"
        cls.index = 0
        return None
    
    @classmethod
    def getCount(cls):
        return [cls.count_new, cls.count_updated]
        
    @classmethod
    def setCount(cls, count_new=None, count_updated=None):
        if count_new != None:
            cls.count_new = count_new 
        if count_updated != None:
            cls.count_updated = count_updated
        return None
    
    @classmethod
    def addCount(cls, count_new=None, count_updated=None):
        if count_new != None:
            cls.count_new += count_new 
        if count_updated != None:
            cls.count_updated += count_updated
        return None
        
    @classmethod
    def resetCount(cls):
        cls.count_new = 0
        cls.count_updated = 0
        cls.placement = None
        return None
        
    @classmethod
    def getPlacement(cls):
        return cls.placement
        
    @classmethod
    def setPlacement(cls, placement=None):
        cls.placement = placement
        return None
            
    # Returns List, Dict, or String
    def checkIf_ListOrDict(self, string):
        try:
            value = ast.literal_eval(string)
        except:
            return string
            
        value_type = type(value ).__name__
        
        # If list, must check if it is only of types (ints, floats) or only strings, not both
        if value_type == "list":
            type_previous = type(value[0] ).__name__
            compatible_types = ["int", "float"]
            is_convertible = True
            
            # excludes 1st index
            for i in value[1:]:
                index_type = type(i ).__name__
                if index_type == type_previous or index_type in compatible_types:
                    continue
                else:
                    is_convertible = False
                    break

            # If types are either (int or float) or just (string), not all 3
            if is_convertible == True:
                return value
            else:
                return string
        elif value_type == "dict":
            return value
        else:
            return string
    
    # Tries to convert Strings into int, floats, dict, or list for Custom Properties
    def valueConvert(self, string):
        value = string
        # int
        try:
            value = int(string)
            return value
        except:
            pass
        # float
        try:
            value = float(string)
            return value
        except:
            pass

        value = self.checkIf_ListOrDict(string )
            
        return value
        
    # To prevent unsafe evaluations and also to be able to add Custom Property to objects with .bl_rna
    def evalSafety(self, string):
        object = None
        # bpy.context.object.data.bones.active.bl_rna.__module__
        # Returns 'bpy_types' or 'bpy.types'
        should_have = ["bpy_types", "bl.types"]

        #Should start with bpy, to prevent malicious code
        if string.startswith("bpy"):
            try:
                object = eval(string)
            except:
                pass#object = None
            
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
        props = scene.PPBR_Props
        
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
        
        if len(props.collection_names) > 0:
        
            # Where to create the Custom Properties
            if props.custom_prop_placement == "OBJECT":
                self.setPlacement( context.object )
            elif props.custom_prop_placement == "DATA":
                self.setPlacement( context.object.data )
            elif props.custom_prop_placement == "SCENE":
                self.setPlacement( context.scene )
            elif props.custom_prop_placement == "WORLD":
                self.setPlacement( context.scene.world )
            # Edit Mode Bone Data
            elif props.custom_prop_placement == "POSE":
                self.setPlacement( context.active_pose_bone )
            # Pose Mode Bone Data
            elif props.custom_prop_placement == "BONE":
                self.setPlacement( context.active_bone )
            #Will be set to "CUSTOM"
            else:
                self.setPlacement( self.evalSafety(props.custom_path) )
                
            if self.getPlacement() != None:
                
                active_index = props.ULIndex_Names
                active_string = props.collection_names[active_index]
                
                def generateProperties(collection_properties, active_string):
                    # scene = bpy.context.scene
                    props = bpy.context.scene.PPBR_Props
                    
                    count_new = 0
                    count_updated = 0
                    # print("MLG: " + str(PROP_BUILDER_OT_generate_custom_props.getPlacement()) )
                    placement = self.getPlacement()
                    
                    #Compiled re.Pattern object
                    patternObject = regexPattern()

                    for i in enumerate(collection_properties):
                    
                        if i[1].use == True:
                            # bpy.context.object["_RNA_UI"] = {"Bruh0": {"min": -1.5, "max": 1.5, "soft_min": 0.5, "use_soft_limits": True} }
                            name_with_prefix = str(i[1].prefix) + active_string.name
                            
                            full_names = [name_with_prefix]

                            if props.generate_flipped == True:
                                name_flipped = flipDirection(name_with_prefix, patternObject)

                                # Append to name_flipped list
                                if name_flipped != None:
                                    full_names.append(name_flipped)
                            
                            for j in full_names:
                                if j not in placement:
                                    placement[j] = self.valueConvert(i[1].value)
                                    
                                    count_new += 1
                                else:
                                    if props.replace_existing_props == True:
                                        placement[j] = self.valueConvert(i[1].value)
                                        
                                    # print("Attribute Exists: %s" % (j) )
                                    count_updated += 1
                                #class 'IDPropertyGroup' is for Custom Properties that are dictionaries
                                if placement[j].__class__.__name__ != 'IDPropertyGroup':
                                    new_dict = {j: {} }
                                    
                                    # This is where all the generated attributes are placed to be created with "_RNA_UI"
                                    for k in attributes:
                                        new_dict[j][k] = getattr(i[1], k)
                                        
                                    placement["_RNA_UI"] = new_dict
                                else:
                                    ##print("Was a dictionary: %s" % (j) )
                                    pass

                    self.addCount(count_new, count_updated)

                    #clears all the "_RNA_UI" dictionary, so it won't stay with the added values
                    placement["_RNA_UI"].clear()
                    return None
                    
                if self.type == "DEFAULT":
                    generateProperties(props.collection_properties, active_string)
                else:
                
                    for i in enumerate(props.collection_names):
                        active_string = props.collection_names[i[0]]
                        
                        generateProperties(props.collection_properties, active_string)
                        
                reportString = "Custom Props: Added New: %d; Updated Existing: %d" % (self.count_new, self.count_updated)
                
                self.resetCount()
                
            # Just error statements
            else:
                if props.custom_prop_placement == "OBJECT":
                    reportString = "No Object selected"
                elif props.custom_prop_placement == "DATA":
                    reportString = "No Object selected"
                elif props.custom_prop_placement == "SCENE":
                    reportString = "No Scene Found"
                elif props.custom_prop_placement == "WORLD":
                    reportString = "No World Found"
                elif props.custom_prop_placement == "POSE":
                    reportString = "No Pose Bone Found"
                elif props.custom_prop_placement == "BONE":
                    reportString = "No Armature Bone Found"
                else:
                    reportString = "Couldn\'t evaluate custom path. Check Console."
        else:
            reportString = "No Property Names to generate from"
            
        self.report({'INFO'}, reportString)
        
        self.type = "DEFAULT"
        
        return {'FINISHED'}

class PROP_BUILDER_OT_transfer_custom_props(bpy.types.Operator):
    bl_idname = "prop_builder.transfer_custom_props"
    bl_label = "Transfer Custom Properties"
    bl_description = "Bruh"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    index: bpy.props.IntProperty(default=0, min=0)
    
    # class variables to count how many new Custom Properties were made
    count_new = 0
    count_updated = 0
    
    # Temporary Class variable where Custom Properties are Transfered "From" & "To"
    placement_to = None
    placement_from = None
    
    @classmethod
    def resetDefaults(cls):
        cls.type = "DEFAULT"
        cls.index = 0
        return None
    
    @classmethod
    def getCount(cls):
        return [cls.count_new, cls.count_updated]
        
    @classmethod
    def setCount(cls, count_new=None, count_updated=None):
        if count_new != None:
            cls.count_new = count_new 
        if count_updated != None:
            cls.count_updated = count_updated
        return None
    
    @classmethod
    def addCount(cls, count_new=None, count_updated=None):
        if count_new != None:
            cls.count_new += count_new 
        if count_updated != None:
            cls.count_updated += count_updated
        return None
        
    @classmethod
    def resetCount(cls):
        cls.count_new = 0
        cls.count_updated = 0
        cls.placement_to = None
        return None
        
    @classmethod
    def getPlacementTo(cls):
        return cls.placement_to
        
    @classmethod
    def setPlacementTo(cls, placement_to=None):
        cls.placement_to = placement_to
        return None
        
    @classmethod
    def getPlacementFrom(cls):
        return cls.placement_from
        
    @classmethod
    def setPlacementFrom(cls, placement_from=None):
        cls.placement_from = placement_from
        return None
            
    # Returns List, Dict, or String
    def checkIf_ListOrDict(self, string):
        try:
            value = ast.literal_eval(string)
        except:
            return string
            
        value_type = type(value ).__name__
        
        # If list, must check if it is only of types (ints, floats) or only strings, not both
        if value_type == "list":
            type_previous = type(value[0] ).__name__
            compatible_types = ["int", "float"]
            is_convertible = True
            
            # excludes 1st index
            for i in value[1:]:
                index_type = type(i ).__name__
                if index_type == type_previous or index_type in compatible_types:
                    continue
                else:
                    is_convertible = False
                    break

            # If types are either (int or float) or just (string), not all 3
            if is_convertible == True:
                return value
            else:
                return string
        elif value_type == "dict":
            return value
        else:
            return string
    
    # Tries to convert Strings into int, floats, dict, or list for Custom Properties
    def valueConvert(self, string):
        value = string
        # int
        try:
            value = int(string)
            return value
        except:
            pass
        # float
        try:
            value = float(string)
            return value
        except:
            pass

        value = self.checkIf_ListOrDict(string )
            
        return value
        
    # To prevent unsafe evaluations and also to be able to add Custom Property to objects with .bl_rna
    def evalSafety(self, string):
        object = None
        # bpy.context.object.data.bones.active.bl_rna.__module__
        # Returns 'bpy_types' or 'bpy.types'
        should_have = ["bpy_types", "bl.types"]

        #Should start with bpy, to prevent malicious code
        if string.startswith("bpy"):
            try:
                object = eval(string)
            except:
                pass#object = None
            
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
        props = scene.PPBR_Props
        
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
        
        #if len(props.collection_names) > 0:
        def getPoseBones(object):
            if context.object.type == "ARMATURE":
                bones = []

                for i in object.pose.bones:
                    if i.bone.select == True:
                        bones.append(i.bone)
                    #object.pose.bones[0].bone.select

                if len(bones) > 0:
                    return bones
                else:
                    return None
            else:
                return None

        def getEditBones(object):
            if context.object.type == "ARMATURE":
                bones = []

                for i in object.pose.bones:
                    if i.bone.select == True:
                        bones.append(i.bone)
                    #object.pose.bones[0].bone.select

                if len(bones) > 0:
                    return bones
                else:
                    return None
            else:
                return None

        # Where to Transfer Custom Properties From
        if props.transfer_from == "OBJECT":
            self.setPlacementFrom( context.object )
        elif props.transfer_from == "DATA":
            self.setPlacementFrom( context.object.data )
        elif props.transfer_from == "SCENE":
            self.setPlacementFrom( context.scene )
        elif props.transfer_from == "WORLD":
            self.setPlacementFrom( context.scene.world )
        # Edit Mode Bone Data
        elif props.transfer_from == "POSE":
            if context.active_object.mode == "POSE":
                self.setPlacementFrom( context.active_pose_bone )
            else:
                pass
        # Pose Mode Bone Data
        elif props.transfer_from == "BONE":
            if context.active_object.mode == "POSE":
                self.setPlacementFrom( context.active_pose_bone.bone )
            else:
                pass
        #Will be set to "CUSTOM"
        else:
            self.setPlacementFrom( self.evalSafety(props.custom_path) )
        
        # Where to Transfer Custom Properties To
        if props.transfer_to == "OBJECT":
            if len(context.selected_objects) > 1:
                self.setPlacementTo( context.selected_objects )
            else:
                self.setPlacementTo( context.object )
            
        elif props.transfer_to == "DATA":
            if len(context.selected_objects) > 1:
                # Just use selected_objects here
                self.setPlacementTo( context.selected_objects )
            else:
                self.setPlacementTo( context.object.data )
            
        elif props.transfer_to == "SCENE":
            self.setPlacementTo( context.scene )
        elif props.transfer_to == "WORLD":
            self.setPlacementTo( context.scene.world )
        # Edit Mode Bone Data
        elif props.transfer_to == "POSE":
            if context.active_object.mode == "POSE":
                selected_bones = context.selected_pose_bones
                #checks if there is more than one active bone
                if len(selected_bones) > 1:
                    self.setPlacementTo( selected_bones )
                else:
                    self.setPlacementTo( context.active_pose_bone)
            else:
                pass
        # Pose Mode Bone Data
        elif props.transfer_to == "BONE":
            if context.active_object.mode == "POSE":
                self.setPlacementTo( context.selected_pose_bones )
            else:
                pass
        # Will be set to "CUSTOM"
        else:
            self.setPlacementTo( self.evalSafety(props.custom_path) )
            
        #This is for Mode Sensitive Stuff
        """
        bpy.context.selected_pose_bones[0].bone
        Results bpy.data.armatures['Armature'].bones["Bone"]

        bpy.context.selected_pose_bones[0]
        Results bpy.data.objects['Armature'].pose.bones["Bone"]
        """
            
        if self.getPlacementFrom() != None and self.getPlacementTo() != None:
            if self.getPlacementFrom() != self.getPlacementTo():
                
                exclude_from = ["_RNA_UI", "cycles_visibility", "cycles"]
                
                properties_from = self.getPlacementFrom().keys()
                
                # Removes exclude_from string from properties_from
                for i in properties_from:
                    if i in exclude_from:
                        properties_from.remove(i)
                
                def generateProperties(placement_from, placement_to):
                    count_new = 0
                    count_updated = 0

                    if len(properties_from) > 0:
                        for i in enumerate(properties_from):
                            print(placement_to.keys())
                            print( str(placement_to)  + ": " + i[1] + ", " + str(i[1] in placement_to) )
                            # If prop already existed
                            if (i[1] in placement_to) == True:
                                print("MLg: 0")
                                # If replacing existing is on
                                if props.replace_existing_props == True:
                                    print("MLg: 1")
                                    del placement_to[ i[1] ]
                                    placement_to[ i[1] ] = placement_from[ i[1] ]
                                    count_updated += 1
                                else:
                                    continue
                            else:   
                                print("MLg: -1")
                                placement_to[ i[1] ] = placement_from[ i[1] ]
                                
                                count_new += 1

                        #Clears the "_RNA_UI" dict from placement_to
                        if "_RNA_UI" in placement_to:
                            placement_to["_RNA_UI"].clear()

                    self.addCount(count_new, count_updated)

                    return None
                    
                def getUniqueObjectData(objects):
                    models = {ob.data for ob in objects}
                    return list(models)
                
                #Returns unique Edit Mode bones
                def getUniqueBones(pose_bones):
                    unique_bones = set()
                    for ob in pose_bones:
                        unique_bones.add(ob.bone )
                    #models = {ob.data for ob in objects}
                    return list(unique_bones)
                    
                placement_from = self.getPlacementFrom()
                placement_to = self.getPlacementTo()

                if props.transfer_from == "OBJECT":
                
                    selected_objects = context.selected_objects
                    
                    # Remove Active object from Selected Object list
                    if props.transfer_to == "OBJECT":
                        if placement_from in selected_objects:
                            selected_objects.remove(placement_from )
                        
                elif props.transfer_from == "DATA":
                
                    selected_objects = getUniqueObjectData(context.selected_objects )
                    
                    # Remove Active object from Selected Object list
                    if props.transfer_to == "OBJECT":
                        if placement_from.data in selected_objects:
                            selected_objects.remove(placement_from.data )
                    elif props.transfer_to == "DATA":
                        if placement_from in selected_objects:
                            selected_objects.remove(placement_from )

                elif props.transfer_from == "POSE":
                    selected_objects = context.selected_pose_bones

                    # Remove Active object from Selected Object list
                    if props.transfer_to == "POSE":
                        if placement_from in selected_objects:
                            selected_objects.remove(placement_from )

                elif props.transfer_from == "BONE":
                    #selected_objects = context.selected_bones
                    selected_objects = getUniqueBones(context.selected_pose_bones )
                    print(selected_objects)
                    
                    # Remove Active object from Selected Object list
                    if props.transfer_to == "BONE":
                        if placement_from in selected_objects:
                            selected_objects.remove(placement_from )

                else:
                    selected_objects = placement_to

                if len(selected_objects) > 0:
                    for i in selected_objects:
                        generateProperties(placement_from, i)

                    #clears all the "_RNA_UI" dictionary, so it won't stay with the added values
                    if "_RNA_UI" in placement_from:
                        placement_from["_RNA_UI"].clear()

                    reportString = "Custom Props: Added New: %d; Updated Existing: %d" % (self.count_new, self.count_updated)
                else:
                    reportString = "Objects were the same"
                
                self.resetCount()
            else:
                reportString = "Transferring From and To are the same location."
            
        # Just error statements
        else:
            #has_active_ob = bpy.context.active_object != None
            #has_selected_ob = len(bpy.context.selected_objects) > len(bpy.context.active_object)
            
            if self.getPlacementFrom() == None:
                if props.transfer_from == "OBJECT":
                    reportString = "No Active Objects"
                elif props.transfer_from == "DATA":
                    reportString = "No Active Object"
                elif props.transfer_from == "SCENE":
                    reportString = "No Scene Found"
                elif props.transfer_from == "WORLD":
                    reportString = "No World Found"
                elif props.transfer_from == "POSE":
                    ## If armature isn't in Pose Mode
                    if context.active_object.mode != "POSE" and context.object.type == "ARMATURE":
                        reportString = "Active Armature not in Pose Mode"
                    else:
                        reportString = "No Active Pose Bone Found"
                elif props.transfer_from == "BONE":
                    reportString = "No Armature Bone Found"
                else:
                    reportString = "Couldn\'t evaluate custom path. Check Console."
            elif self.getPlacementTo() == None:
                if props.transfer_to == "OBJECT":
                    reportString = "No Selected Object"
                elif props.transfer_to == "DATA":
                    reportString = "No Selected Object"
                elif props.transfer_to == "SCENE":
                    reportString = "No Scene Found"
                elif props.transfer_to == "WORLD":
                    reportString = "No World Found"
                elif props.transfer_to == "POSE":
                    ## If armature isn't in Pose Mode
                    if context.active_object.mode != "POSE" and context.object.type == "ARMATURE":
                        reportString = "Active Armature not in Pose Mode"
                    else:
                        reportString = "No Active Pose Bone Found"
                elif props.transfer_to == "BONE":
                    reportString = "No Armature Bone Found"
                else:
                    reportString = "Couldn\'t evaluate custom path. Check Console."
            
        self.report({'INFO'}, reportString)
        
        self.type = "DEFAULT"
        
        return {'FINISHED'}

# List drawing Class
class PROP_BUILDER_UL_items_strings(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.PPBR_Props
        
        # active = props.RIA_ULIndex
        RPMR_Collection = props.collection_names
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(RPMR_Collection) > 0:
                row.prop(item, "name", text="", emboss=False)
                
            else:
                row.label(text="No Iterations Here")
                
        # Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass
        
# List drawing Class
class PROP_BUILDER_UL_items_properties(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.PPBR_Props
        
        # active = props.RIA_ULIndex
        RPMR_Collection = props.collection_names
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(RPMR_Collection) > 0:
                row.prop(item, "use", text="", emboss=True)
                row.prop(item, "name", text="", emboss=False)
                
            else:
                row.label(text="No Iterations Here")
                
        # Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass

class PROP_BUILDER_MT_dropdown_menu_ui_generate(bpy.types.Menu):
    bl_idname = "PROP_BUILDER_MT_dropdown_menu_ui_generate"
    bl_label = "Extra UI Functions & Operators"
    bl_description = "Extra functions for generating Custom Properties"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        data = bpy.data
        props = scene.PPBR_Props
        
        col = layout.column()
        
        # row = col.row(align=True)
        button = col.operator("prop_builder.generate_custom_props", icon="ADD", text="For All Names")
        button.type = "ALL"
        

class PROP_BUILDER_MT_dropdown_menu_ui_properties(bpy.types.Menu, customMethods):
    bl_idname = "PROP_BUILDER_MT_dropdown_menu_ui_properties"
    bl_label = "Extra UI Functions & Operators"
    bl_description = "Copy/Paste and Duplicate functions"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.PPBR_Props
        
        col = layout.column()
        
        # row = col.row(align=True)
        
        properties = {"collection": "collection_properties", "list_index": "ULIndex_Properties"}
        
        # Copy/Paste
        button = col.operator("prop_builder.copy_paste_prop", text="Copy", icon="COPYDOWN")
        button.type = "COPY"
        
        button = col.operator("prop_builder.copy_paste_prop", text="Paste", icon="PASTEDOWN")
        button.type = "PASTE"
        
        button = col.operator("prop_builder.general_ui_ops", text="Duplicate", icon="DUPLICATE")
        self.setAttributes(button, properties)
        button.type = "DUPLICATE"

class PROP_BUILDER_PT_transfer_props(bpy.types.Panel, customMethods):
    # A Custom Panel in Viewport
    bl_idname = "PROP_BUILDER_PT_transfer_props"
    bl_label = "Property Transfer"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # bl_context = "output"
    bl_category = "Prop Build"
    
    # collectionOOF: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        scene = context.scene
        props = scene.PPBR_Props
        
        # Layout Starts
        col = layout.column()
        
        # Active Collection
        row = col.row(align=True)
        row.label(text="Transfer Properties:")
        
        row = col.row(align=True)
        row.prop(props, "transfer_from", text="From", expand=False)
        
        row = col.row(align=True)
        row.prop(props, "transfer_to", text="To", expand=False)
        
        row = col.row(align=True)
        row.operator("prop_builder.transfer_custom_props", text="Transfer", icon="TRIA_DOWN")
        
        # End of CustomPanel

class PROP_BUILDER_PT_custom_panel1(bpy.types.Panel, customMethods):
    # A Custom Panel in Viewport
    bl_idname = "PROP_BUILDER_PT_custom_panel1"
    bl_label = "Property Builder"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # bl_context = "output"
    bl_category = "Prop Build"
    
    # collectionOOF: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        scene = context.scene
        props = scene.PPBR_Props
        
        # Layout Starts
        col = layout.column()
        
        # Active Collection
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
            
        row.operator("prop_builder.generate_custom_props", icon="ADD", text="For Active Name")
        # Copy/Paste Menu
        row.menu("PROP_BUILDER_MT_dropdown_menu_ui_generate", icon="DOWNARROW_HLT", text="")
        
        # Separates for extra space between
        col.separator()
            
        # Duplicate Button BOTTOM
        
        row = col.row(align=True)
        row.label(text="Property Names: %d" % (len(props.collection_names) ) )
        
        # row = col.row(align=True)
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("PROP_BUILDER_UL_items_strings", "custom_def_list", props, "collection_names", props, "ULIndex_Names", rows=3)
        
        # Side_Bar Operators
        col = split.column(align=True)
        
        properties = {"collection": "collection_names", "list_index": "ULIndex_Names"}
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="ADD")
        self.setAttributes(button, properties)
        button.type = "ADD"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="TRIA_UP")
        self.setAttributes(button, properties)
        button.type = "UP"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="TRIA_DOWN")
        self.setAttributes(button, properties)
        button.type = "DOWN"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="PANEL_CLOSE")
        self.setAttributes(button, properties)
        button.type = "REMOVE"
        
        
        
        col = layout.column()
        
        
        col.separator()
            
        # Duplicate Button BOTTOM
        
        row = col.row(align=True)
        row.label(text="Properties: %s" % (len(props.collection_properties) ))
        
        # row = col.row(align=True)
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("PROP_BUILDER_UL_items_properties", "custom_def_list", props, "collection_properties", props, "ULIndex_Properties", rows=3)
        
        # Side_Bar Operators
        col = split.column(align=True)
        
        properties = {"collection": "collection_properties", "list_index": "ULIndex_Properties"}
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="ADD")
        self.setAttributes(button, properties)
        button.type = "ADD"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="TRIA_UP")
        self.setAttributes(button, properties)
        button.type = "UP"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="TRIA_DOWN")
        self.setAttributes(button, properties)
        button.type = "DOWN"
        
        button = col.operator("prop_builder.general_ui_ops", text="", icon="PANEL_CLOSE")
        self.setAttributes(button, properties)
        button.type = "REMOVE"
        
        # Copy/Paste Menu
        col.menu("PROP_BUILDER_MT_dropdown_menu_ui_properties", icon="DOWNARROW_HLT", text="")
        
        # End of CustomPanel
        

# This is a subpanel
class PROP_BUILDER_PT_property_editor(bpy.types.Panel, customMethods):
    bl_label = "Property"
    bl_parent_id = "PROP_BUILDER_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # bl_context = "output"
    bl_category = "Prop Build"
    
    def draw(self, context):
        layout = self.layout
        
        data = bpy.data
        scene = context.scene
        props = scene.PPBR_Props
        
        active_index = props.ULIndex_Properties
        
        col = layout.column()
        
        if len(props.collection_properties) > 0:
            
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
            
            button = col.operator("prop_builder.general_ui_ops", text="Add Properties to edit", icon="ADD")
            self.setAttributes(button, properties)
            button.type = "ADD"
            # row.label(text="Add Properties to edit")
            # row.enabled = False

    ## End of Subpanel

            
# This is a subpanel
class PROP_BUILDER_PT_options(bpy.types.Panel, customMethods):
    bl_label = "Options"
    bl_parent_id = "PROP_BUILDER_PT_custom_panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # bl_context = "output"
    bl_category = "Prop Build"
    
    def draw(self, context):
        layout = self.layout
        
        data = bpy.data
        scene = context.scene
        props = scene.PPBR_Props
        
        active_index = props.ULIndex_Properties
        
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Generated Properties")

        row = col.row(align=True)
        # row.label(text="Add Button to 3D Viewport Header?")
        row.prop(props, "replace_existing_props", expand=True, text="Update Existng")

        row = col.row(align=True)
        # row.label(text="Add Button to 3D Viewport Header?")
        row.prop(props, "generate_flipped", expand=True, text="Generate Flipped L/R")
        


class PROP_BUILDER_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    # here you define the addons customizable props
    ui_tab: bpy.props.EnumProperty(name="Enum", items= [("GENERAL", "General", "General Options"), ("ABOUT", "About", "About Author & Where to Support")], description="Backup Object UI Tabs", default="GENERAL")
    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        props = scene.PPBR_Props
        
        col = layout.column()
        
        row = col.row(align=True)
        row.prop(self, "ui_tab", expand=True)
        row = col.row(align=True)
        
        box = layout.box()
        col = box.column()
        
        if self.ui_tab == "GENERAL":
            row = col.row(align=True)
            # row.label(text="Add Button to 3D Viewport Header?")
            row.prop(props, "replace_existing_props", expand=True, text="Replace/Update Existng Properties")
            
            row = col.row(align=True)
            row.prop(props, "generate_flipped", expand=True, text="Generate Flipped L/R Properties")
            
        elif self.ui_tab == "ABOUT":
            row = col.row(align=True)
            row.label(text="JohnGDDR5 on: ")
            row.operator("wm.url_open", text="Youtube").url = "https://www.youtube.com/channel/UCzPZvV24AXpOBEQWK4HWXIA"
            row.operator("wm.url_open", text="Twitter").url = "https://twitter.com/JohnGDDR5"
            row.operator("wm.url_open", text="Artstation").url = "https://www.artstation.com/johngddr5"


# Classes that are registered
classes = (
    PROP_BUILDER_properties,
    PROP_BUILDER_property_names,
    PROP_BUILDER_props,

    PROP_BUILDER_OT_general_ui_ops,
    
    PROP_BUILDER_OT_copy_paste_prop,
    PROP_BUILDER_OT_generate_custom_props,
    PROP_BUILDER_OT_transfer_custom_props,

    PROP_BUILDER_UL_items_strings,
    PROP_BUILDER_UL_items_properties,
    
    PROP_BUILDER_MT_dropdown_menu_ui_generate,
    PROP_BUILDER_MT_dropdown_menu_ui_properties,
    
    PROP_BUILDER_PT_transfer_props,
    PROP_BUILDER_PT_custom_panel1,
    PROP_BUILDER_PT_property_editor,
    PROP_BUILDER_PT_options,

    PROP_BUILDER_preferences
)

