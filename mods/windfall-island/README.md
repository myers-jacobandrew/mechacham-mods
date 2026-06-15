# Windfall Island

Windfall Island from *The Legend of Zelda: The Wind Waker*, as a custom Meccha Chameleon map.

[Steam Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745643656)

## status

v1 is up. known issues:

- no ocean (might pull water from [BeamMan3's water pack](https://uu.getuploader.com/BeamMan3/download/143) later, need to research)
- windmill is missing (separate `.obj` in the source bundle, didn't bring it in for v1)
- materials are just base color, no normals or specular

might fix in a future update maybe.

## credits

- Nintendo (original game)
- Peardian and TwilightRipper, model rip from [The Models Resource](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/)

## source

Model bundle from [The Models Resource](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/). It's a zip with `.obj` / `.dae` / `.mtl` plus PNG textures.

Water (future): [BeamMan3 water pack](https://uu.getuploader.com/BeamMan3/download/143). Not used yet, still figuring out if it'll work.

## how it was built

1. download and extract the Models Resource zip.
2. drag the main island `.obj` into the UE Content Browser. UE imports OBJ natively as a Static Mesh.
3. drag the PNGs into the same folder. UE imports them as Textures.
4. wire textures into the material Base Color slots. either manually, or via `tools/wire_materials.py` with a hand-written manifest.
5. place the static mesh in the level. SkyAtmosphere + DirectionalLight + SkyLight for lighting.
6. (skipped for v1: ocean. UE Water plugin was attempted but had transparency / shadow / void issues that weren't worth fighting before first ship.)
7. cook + package per [`docs/BUILD.md`](../../docs/BUILD.md).

## level details

- PlayerStart at (0, 0, 100) per modkit spec.
- camera collision profile: `CameraBlockWall` on island geometry.
