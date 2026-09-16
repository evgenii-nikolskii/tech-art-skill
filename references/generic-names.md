# Generic and Suspicious Names

This is a detection vocabulary for names that may indicate an asset was not renamed after creation, export, duplication, or import.

These names are signals, not automatic proof of a problem. The skill must consider the asset type, project convention, surrounding names, references, and whether the token is part of a meaningful compound name.

## High-confidence generic names

These are usually non-descriptive when used as a complete asset, object, material, mesh, texture, collection, or folder name:

### Creation and placeholder names

```text
new
newasset
new asset
newfile
new file
newfolder
new folder
newmaterial
new material
newmesh
new mesh
newtexture
new texture
untitled
unnamed
unknown
default
standard
placeholder
dummy
sample
example
test
testing
temp
tmp
work
wip
todo
```

### Generic asset-type names

```text
asset
file
data
object
objects
element
elements
item
items
resource
resources
model
models
mesh
meshes
geo
geometry
material
materials
mat
mats
texture
textures
tex
image
images
image_texture
imagetexture
map
maps
shader
shaders
surface
node
nodes
group
groups
collection
collections
folder
folders
scene
scenes
level
levels
prefab
prefabs
```

### Primitive and default scene names

```text
cube
plane
sphere
uvsphere
ico_sphere
icosphere
cylinder
cone
torus
circle
grid
quad
capsule
camera
light
empty
null
locator
joint
root
origin
```

### Maya-style defaults

```text
pcube1
psphere1
pcylinder1
pcone1
plane1
polySurface1
polySurface2
lambert1
blinn1
phong1
initialShadingGroup
initialParticleSE
```

### 3ds Max-style defaults

```text
box001
sphere001
sphere030
cylinder001
cone001
plane001
teapot001
geosphere001
shape001
line001
```

### Blender-style defaults

```text
cube.001
cube.002
plane.001
sphere.001
camera.001
light.001
collection
material.001
material.002
```

### Unreal and engine primitive names

```text
cube
sphere
cylinder
cone
plane
defaultmaterial
default material
newmaterial
new material
```

## Numeric and duplication patterns

These patterns are suspicious when they are the entire name or are attached to an otherwise generic name:

```text
001
002
01
02
0001
1
2
asset001
object001
mesh001
model001
material001
texture001
copy
copy1
copy_1
copy of *
duplicate
duplicate1
backup
backup1
old
old1
new1
new2
final
final1
final2
final_final
final_final2
version1
version2
v1
v2
rev1
rev2
```

The numeric suffix itself is not automatically invalid. It becomes a warning when there is no meaningful base name, when numbering is inconsistent, or when it appears to be an automatic collision suffix such as `.001`, `001`, or `1`.

## Suspicious workflow and export words

These words are not always wrong, but should trigger a warning when they are the only meaningful part of a name or are repeated across many assets:

```text
export
exported
import
imported
bake
baked
base
source
target
input
output
in
out
temp
tmp
test
testing
debug
fix
fixed
backup
old
copy
duplicate
untitled
scene
file
asset
data
```

## Generic type prefixes and suffixes

These are suspicious only when they replace an actual descriptive name:

```text
mat_
material_
tex_
texture_
mesh_
model_
object_
geo_
geo_
img_
image_
map_
shader_
asset_
new_
temp_
tmp_
test_
copy_
duplicate_
final_
v01
_mat
_material
_tex
_texture
_mesh
_model
_geo
_map
_copy
_final
```

An engine convention such as Unreal's `M_`, `MI_`, `SM_`, `SK_`, or `T_` is not generic noise by itself when followed by a meaningful asset name. It should be evaluated against the project's established convention.

## Detection notes

- Compare case-insensitively.
- Normalize spaces, hyphens, underscores, and dots before matching where appropriate.
- Detect exact names separately from names that merely contain a generic token.
- Do not flag meaningful names such as `Stone_Material`, `CubeRoom`, `TextureAtlas`, or `FinalBoss` solely because they contain a generic word.
- Treat names inside imported model metadata, material slots, node graphs, collections, and folders with the same scrutiny as filesystem asset names.
- Report the original name, asset type, path, and the matched rule.
- Do not rename anything automatically.

## Official examples of application-generated names

- Blender documents automatic collision suffixes such as `Cube.001`.
- Maya documents default nodes such as `lambert1` and object names such as `pSphere1`.
- 3ds Max documents primitive defaults such as `Box001` and `Sphere030`.
- Unity documents generated names such as `NewFolder` and material naming based on model, material, or texture names.
- Unreal documents default primitive assets such as `Cube`, `Sphere`, `Cylinder`, `Cone`, and `Plane`.

## Sources

- [Blender Data-Block Menu](https://docs.blender.org/manual/en/2.90/interface/controls/templates/data_block.html)
- [Autodesk Maya: Lambert](https://help.autodesk.com/cloudhelp/2022/ENU/Maya-LightingShading/files/GUID-97B781A0-7F21-42D4-B040-8EB967CB8563.htm)
- [Autodesk Maya: File referencing and shading](https://help.autodesk.com/cloudhelp/2022/ENU/Maya-ManagingScenes/files/GUID-83E8811C-BEE2-4753-8F83-4E9EEE66D7DD.htm)
- [Autodesk 3ds Max: Standard primitives](https://help.autodesk.com/cloudhelp/2023/ENU/3DSMax-Modeling/files/GUID-46FD7C8B-7710-4B61-9A14-C8F385D255B0.htm)
- [Unity: AssetDatabase](https://docs.unity3d.com/cn/6000.0/Manual/AssetDatabase.html)
- [Unity: Model importer material naming](https://docs.unity3d.com/cn/2022.3/ScriptReference/ModelImporterMaterialName.html)
- [Unreal Engine: Static Mesh Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/static-mesh-actors-in-unreal-engine)
- [Unreal Engine: Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)
