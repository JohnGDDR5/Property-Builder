
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

##Note: Soft_min and max should be between the range of the min and the max, or else "use_soft_limits" won't work, and the soft_min and max won't be assigned.