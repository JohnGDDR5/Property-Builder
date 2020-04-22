
## These notes are to be address the differences between accesssing Pose and Edit bones from Pose and Edit mode.

Pose Bones are relative to the Armature "Object" not the Data. Custom Properties will always be unique as it is tied to an Object
Bones are relative to the Armature "Data"
Edit_Bones are relative to Armature "Data", only accessible in Edit Mode, and give extra info such as Active Edit Bone

So, the most useful ones are Pose & Bones.

## Pose Mode
bpy.context.object.pose.bones
Returns bpy.data.objects['Armature'].pose.bones

bpy.context.object.pose.bones[0].bone
Returns bpy.data.armatures['Armature'].bones["Bone"]

## Access Custom properties of Pose Mode bones
bpy.context.object.pose.bones[0].bone["prop"]
Returns 1.0

bpy.context.object.pose.bones[0]['prop']
Returns 1.0

## Active Pose Bone
bpy.context.active_pose_bone
Returns bpy.data.objects['Armature'].pose.bones["Bone.001"]

bpy.context.object.data.bones[1].select
Return True

## Pose Bone Custom Properties
bpy.context.object.data.bones[0]['prop']
bpy.data.objects['Armature'].pose.bones["Bone.001"]["prop"]

## Edit Mode

## Custom Prop of Edit Bone
bpy.data.armatures['Armature'].bones['Bone']['prop']

## How to get Active bone in Edit Mode
bpy.data.armatures['Armature'].edit_bones.active.name
Returns "Bone.001" .etc

## Iterate through Edit Mode bones
bpy.data.armatures['Armature'].edit_bones[0].select
Returns True

## Access Custom properties of Edit Mode bones
bpy.data.armatures['Armature'].edit_bones[0]['prop']
Returns 1.0

## Note for some reason, we can't iterate through edit_bones unless we are in Edit Mode
bpy.context.object.data.edit_bones[0]

##Object Mode
bpy.context.active_bone
Returns bpy.data.objects['Armature'].pose.bones["Bone.001"]