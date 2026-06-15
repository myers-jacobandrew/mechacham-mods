# Windfall Island

Windfall Island from *The Legend of Zelda: The Wind Waker*, as a Meccha Chameleon custom map.

**[Steam Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745643656)**

## Status

v1 published. Known issues:

- **Windmill missing.** The MMD (.pmx) source used for this version only includes the central island; the windmill is a separate prop in the original game model and didn't import. v2 will add it (import the [Models Resource model](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/) which has it as a separate .obj part).
- Some texture/material wiring is approximate (only base color, no normals/specular maps).

## Credits

- Nintendo — original game
- Peardian and TwilightRipper — model rip ([The Models Resource](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/))

## Build pipeline

This mod was built from a MikuMikuDance `.pmx` rip using:

1. `tools/pmx_to_fbx.py` — convert PMX to FBX in Blender (mmd_tools), dump material→texture manifest to `tools/windfall_material_textures.json`
2. UE import: FBX as Static Mesh (Force All Mesh as Type → Static Mesh), Bake Meshes ✅, Vertex Color Replace
3. Manually drag-import 30 PNG textures into UE (FBX importer dropped most of mmd_tools's texture refs)
4. `tools/wire_materials.py` (run from UE Python console) — reads the manifest, wires each Texture to its Material's Base Color slot
5. Place the static mesh actor in the level, add WaterBodyOcean + WaterZone for the ocean, set up SkyAtmosphere + DirectionalLight + SkyLight
6. Cook + package per [`docs/BUILD.md`](../../docs/BUILD.md)

## Level details

- PlayerStart at (0, 0, 100) per modkit spec
- WaterBodyOcean with bounded spline ~around the island
- A flat ground plane sits underneath as the "missing seafloor" (the Water plugin's water is transparent at grazing angles, and without a seafloor mesh you see straight through into the void)
- Camera collision profile: `CameraBlockWall` on island geometry
