# BlenderMixamo2glTFConverter

Script to convert mixamo fbx to a gltf which only contains the animation track

Exported animation clip should be compatible with any rig which follows the same bone naming structure and bone rotations

Demo https://y9cs7m.csb.app/
Code https://codesandbox.io/s/separate-animations-test-y9cs7m?file=/src/index.js

## Instructions

- download everything
- update the path to the script
- create a "fbx_input" folder where you can dump all the mixamo fbxs
- create a "gltf_output" where the script can export gltf(.glb) files
- open a fresh blend file
- copy the script in the scripting layout
- run script

On windows make this script run via cmd using a `.bat` file for easy re-use

## what the script does

- import fbx from provided path with 0 time offset so animations start at frame 0 (blender's time is also set to start from 0)
- fix the scale and rotation issues in the bones as well as in the keyframes
- remove location and scale keyframes so it should be compatible with different sized rigs (since animations are 99% driven by bone rotations)
- export gltf to specified directory with sampling off
- fbx file's name will become gltf animation clip's name as well as the gltf file name

## Extras

Use `bone_rename.py` to remove all the phrase "mixamo:" from the bone names
