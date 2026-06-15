# Windfall Island

Windfall Island from *The Legend of Zelda: The Wind Waker*, as a custom Meccha Chameleon map.

[Steam Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745643656)

## status

v1 is up. known issues:

- windmill is missing (it's a separate `.obj` in the source bundle, didn't bring it in for v1). maybe a future update.
- materials are just base color, no normals or specular.

## credits

- Nintendo (original game)
- Peardian and TwilightRipper, model rip from [The Models Resource](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/)

## source

Model bundle from [The Models Resource](https://models.spriters-resource.com/gamecube/thelegendofzeldathewindwaker/asset/313489/). It's a zip with `.obj` / `.dae` / `.mtl` plus PNG textures.

## how it was built

1. download + extract the Models Resource zip.
2. drag the main island `.obj` into the UE Content Browser. UE imports OBJ natively as a Static Mesh.
3. drag the PNGs into the same folder. UE imports them as Textures.
4. wire textures into the material Base Color slots. either manually, or via `tools/wire_materials.py` with a hand-written manifest.
5. place the static mesh in the level. add WaterBodyOcean + WaterZone for the ocean. SkyAtmosphere + DirectionalLight + SkyLight for lighting. drop a flat plane under sea level so you don't see through the transparent water into the void.
6. cook + package per [`docs/BUILD.md`](../../docs/BUILD.md).

## level details

- PlayerStart at (0, 0, 100) per modkit spec.
- WaterBodyOcean spline around the island.
- flat plane below water as a seafloor backdrop.
- camera collision profile: `CameraBlockWall` on island geometry.
