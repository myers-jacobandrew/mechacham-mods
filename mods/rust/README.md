# Rust - MW2

Rust from *Call of Duty: Modern Warfare 2* (2009), as a custom Meccha Chameleon map.

[Steam Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3746267362)

## status

up and playable. notes:

- a couple material slots use best-guess stand-in textures (a few originals weren't in the export)
- the packed COD spec maps were skipped, just color + normal for now
- expect some jank

## credits

- Infinity Ward / Activision (original game)

## source

MW2 2009 rip: a `.blend` with the `mp_rust` map mesh, plus a folder of `.TGA` textures (color `_col` and normal `_nml` maps). Raw source isn't committed here, just the imported UE assets.

## how it was built

1. import the `mp_rust` mesh into the UE Content Browser (Static Mesh).
2. import the `.TGA` textures; flag the `_nml` ones as normal maps.
3. one master material (BaseColor + Normal), then a Material Instance per texture set, matched to the mesh's 68 slots by name (scripted with a python wiring pass).
4. World Partition map with streaming off, per modkit spec.
5. center the compound on world origin so the fixed (0,0,100) spawn lands on the floor.
6. collision: Use Complex Collision As Simple + `CameraBlockWall` on the mesh.
7. 4 invisible blocking walls around the perimeter so players can't wander off.
8. light sepia post-process grade.
9. cook + package per [`docs/BUILD.md`](../../docs/BUILD.md).

## level details

- spawn at (0, 0, 100) per modkit spec.
- camera collision profile: `CameraBlockWall` on the map mesh.
- invisible perimeter walls keep players inside the compound.
