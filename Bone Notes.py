
## These notes are to be address the differences between accesssing Pose and Edit bones from Pose and Edit mode.

## Pose Mode
bpy.context.object.pose.bones
Returns bpy.data.objects['Armature'].pose.bones

bpy.context.object.pose.bones[0].bone
Returns bpy.data.armatures['Armature'].bones["Bone"]

## Access Custom properties of Pose Mode bones
bpy.context.object.pose.bones[0].bone["prop"]
Returns 1.0

## Active Pose Bone
bpy.context.active_pose_bone
Returns bpy.data.objects['Armature'].pose.bones["Bone.001"]

## Edit Mode

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