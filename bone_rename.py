import bpy
selected_objects = bpy.context.selected_objects

for obj in selected_objects:
    if obj.type == 'ARMATURE':
        for bone in obj.data.bones:
            print('Removing the phrase "mixamorig:" from ', bone.name)
            new_name = bone.name.replace('mixamorig:', '')
            bone.name = new_name
