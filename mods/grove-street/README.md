# Grove Street

Grove Street from *GTA: San Andreas*, as a custom Meccha Chameleon map.

[Steam Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745770286)

## status

v1 is up. known issues:

- map might be a bit big
- giant void around the neighborhood. ignore it for now, maybe box it in later
- this whole thing is rough, expect jank
- materials are base color only

## credits

- Rockstar Games (original game)
- [paltoandr7](https://sketchfab.com/3d-models/gtasa--grove-street-v2-e778c61799434ccdad0a1963a11aeb7e) for the GTASA Grove Street v2 model (CC Attribution, Sketchfab)

## how it was built

OBJ source from Sketchfab, ZIP contained `.obj` / `.mtl` + 94 PNG textures (plus duplicate TGAs we ignored).

1. Stage source: copy OBJ + MTL + PNGs to a clean folder. Patch the OBJ's `mtllib` line to reference the local MTL.
2. Run `tools/obj_to_fbx.py` in Blender. It imports the OBJ, joins all mesh objects into one, dumps a material to texture manifest JSON, exports as FBX.
   - This step is required because importing the raw OBJ into UE 5.6 crashes the mesh importer (`MeshElementIndexer.cpp` assert) on big OBJs with many groups.
3. Drag the FBX into UE. Force Static Mesh, Combine Meshes on. ~1855 material slots get created.
4. Drag the 94 PNGs into UE as Textures.
5. Run `tools/wire_materials.py` from UE's Python console with the Grove Street manifest. It wires every material's Base Color to its PNG via the manifest.
6. Place the static mesh in the level. Add lighting. Position so spawn (0, 0, 100) lands somewhere walkable.
7. Cook + package per [`docs/BUILD.md`](../../docs/BUILD.md).

## level details

- PlayerStart at (0, 0, 100) per modkit spec
- Big void around the playable area, no boundary mesh yet
- Camera collision profile: `CameraBlockWall` on the static mesh
