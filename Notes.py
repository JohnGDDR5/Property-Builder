

bpy.types.RIG_PROP_MAN_OT_general_ui_ops.mro()
Returns the class and subclasses of the class
[<class '__main__.RIG_PROP_MAN_OT_general_ui_ops'>, <class 'bpy_types.Operator'>, <class 'bpy_struct'>, <class '__main__.customMethods'>, <class 'object'>]

##You can create a new property available for all class types, that is unique for all of them

##Ex. For bpy.types.Object

#Initialize with variable
bpy.types.Object.test_bruh = bpy.props.BoolProperty(name="Dropdown", default=False)

#So, now every Object will have a unique Boolean that can be toggled. 
bpy.context.object.test_bruh
#Returns: False, as this is the default

#Can be changed
bpy.context.object.test_bruh = True

##To remove the custom API-Defined class property, just delete items
del bpy.types.Object.test_bruh

##To Create and Access Custom Properties and their Min/Max values

##Use the "_RNA_UI" dictionary, which stores all the properties of a custom property


##To edit the Min/Max values of a Custom Property, 
1st Initialize the Custom Property, then use "_RNA_UI" to edit the Custom Prop, or else it won't work
bpy.context.object["Bruh0"] = 1

bpy.context.object["_RNA_UI"] = {"Bruh0": {"min": -1.5, "max": 1.5, "soft_min": 0.5, "use_soft_limits": True} }
bpy.context.object["_RNA_UI"] = {"Bruh6": {"TRASH": True} }

##Note: Soft_min and max should be between the range of the min and the max, or else "use_soft_limits" won't work, and the soft_min and max won't be assigned.

##To access the custom properties of an object
.items()

bpy.context.object.items()
Returns
[('_RNA_UI', <bpy id prop: owner="OBCube", name="_RNA_UI", address=0x000001794C9DA1E8>), ('Bruh2', 'oof'), ('Bruh3', <bpy id prop: owner="OBCube", name="Bruh3", address=0x000001794C9DA6F8>), ('trash_bruh', 1), ('prop', 'Color(0, 0, 0, 0)'), ('Bruh', 1), ('Bruh0', 1.0), ('cycles_visibility', <bpy id prop: owner="OBCube", name="cycles_visibility", address=0x000001795C08B728>), ('cycles', <bpy id prop: owner="OBCube", name="cycles", address=0x000001795C08D468>)]

bpy.context.object.keys()
For List of all Custom Properties Names
Returns 
['_RNA_UI', 'Bruh2', 'Bruh3', 'trash_bruh', 'prop', 'Bruh', 'Bruh0', 'cycles_visibility', 'cycles'

##For Custom Properties that have been assigned a Dictionary
Ex. bpy.context.object["Bruh3"] = {'default': 1}

bpy.context.object["Bruh3"]
Returns this <bpy id prop: owner="OBCube", name="Bruh3", address=0x000001794C9DA6F8>

bpy.context.object["Bruh3"].to_dict() 
Returns dictionary {'default': 1}

Same as dict(bpy.context.object["Bruh3"])
Returns dictionary {'default': 1}

type(bpy.context.object["Bruh3"]) ##Bruh0 is a dictionary, and its type returns this
Returns <class 'IDPropertyGroup'>

bpy.context.object["Bruh6"].__class__.__name__
Returns name 'IDPropertyGroup'

type(bpy.context.object["Bruh0"]) ##Bruh0 is an integer, not dict
Returns <class 'float'>


##Prints matrices of object
def oof():
    bruh = [
    bpy.context.object.matrix_basis,
    bpy.context.object.matrix_local,
    bpy.context.object.matrix_parent_inverse,
    bpy.context.object.matrix_world,
    ]
    for i in bruh:
        print(i)
