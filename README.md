# BlenderMixamo2glTFConverter

Script to convert mixamo fbx to a gltf which only contains the animation track 

Exported animation clip should be compatible with any rig which follows the same bone naming structure and bone rotations

Instructions
- create a inputFolder where you can dump all the mixamo fbxs
- create a outputFolder where the script can export gltf(.glb) files 
- open a fresh blend file 
- copy the script in the scripting layout
- update the path to the fbx folder and output folder in the script
- run script



what the script does 
- import fbx from provided path with 0 time offset so animations start at frame 0 (blender's time is also set to start from 0) 
- fix the scale and rotation issues in the bones as well as in the keyframes
- remove location and scale keyframes so it should be compatible with different sized rigs (since animations are 99% driven by bone rotations)
- export gltf to specified directory 
- fbx file's name will become gltf animation clip's name 
