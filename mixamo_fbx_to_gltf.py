import bpy
import os
import json
os.system('cls')  # clears console

# Specify the path to the directory where your script is located
script_dir = r'F:\net\BlenderMixamo2glTFConverter/'

# Construct paths to dirs based on the script's location
fbx_dir = os.path.join(script_dir, 'fbx_input/')
export_dir = os.path.join(script_dir, 'gltf_output/')

print(script_dir, fbx_dir, export_dir)

# clears all blend file contents so old content does not pile up and interfere with renaming


def clear_blend_file():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # prevent old actions from piling up
    for action in bpy.data.actions:
        action.use_fake_user = False

    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True)


# Check if the fbx_dir exists
if os.path.exists(fbx_dir) and os.path.isdir(fbx_dir):
    # List all files in the directory with .fbx extension
    fbx_files = [file for file in os.listdir(
        fbx_dir) if file.lower().endswith('.fbx')]
    print("Found FBX files:", fbx_files)
else:
    print("FBX directory does not exist:", fbx_dir)


for i, fbx_name in enumerate(fbx_files):
    print(i, fbx_name)

    name = os.path.splitext(os.path.basename(fbx_name))[0]
    gltf_path = export_dir+name+'.glb'
    if os.path.exists(gltf_path):
        print('Skipping ', name)
        continue

    clear_blend_file()
    fbx_path = fbx_dir+fbx_name

    # import fbx with 0 anim offset so looping animations work correctly
    bpy.ops.import_scene.fbx(filepath=fbx_path, anim_offset=0.0)

    longest_duration = 0
    armature_obj = bpy.data.objects['Armature']

    animation_data = armature_obj.animation_data

    # rename bones
    for bone in armature_obj.data.bones:
        new_name = bone.name.replace('mixamorig:', '')
        bone.name = new_name

    # Rename Animation
    if animation_data is not None and animation_data.action is not None:
        animation_data.action.name = name

    # Fix scale and rotation
    bpy.ops.object.transform_apply(
        location=False, rotation=True, scale=True)

    all_curves = []

    for curve in armature_obj.animation_data.action.fcurves:
        all_curves.append(curve)

    for curve in all_curves:
        # print(curve,curve.data_path)

        for keyframe in curve.keyframe_points:
            if curve.data_path.endswith(".location"):
                keyframe.co[1] *= 0.010

            if keyframe.co[0] > longest_duration:
                longest_duration = keyframe.co[0]

    # Delete useless location and scale keyframes ?
    fcs = armature_obj.animation_data.action.fcurves
    for fc in fcs:
        if fc.data_path.endswith(".location") and not "Hips" in fc.data_path:
            fcs.remove(fc)
        elif fc.data_path.endswith(".scale"):
            fcs.remove(fc)

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = int(longest_duration)

    action = armature_obj.animation_data.action

    # Create a new NLA track for the action
    nla_track = armature_obj.animation_data.nla_tracks.new()
    nla_track.name = name

    # Create a new NLA strip for the action in the track
    strip = nla_track.strips.new(action.name, 0, action)
    strip.name = action.name

    export_path = export_dir+name

    # export gltf with sampling off so that the deleted keyframes don't get added again
    bpy.ops.export_scene.gltf(
        filepath=export_path, export_force_sampling=False)
