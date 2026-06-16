# mechacham-mods

My custom maps for Meccha Chameleon. Built with the MecchaChameleon Custom Mod Kit, uploaded to Steam Workshop.

## mods

| mod | workshop | status |
|---|---|---|
| [Windfall Island](mods/windfall-island/) | [link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745643656) | v1, windmill missing |
| [Grove Street](mods/grove-street/) | [link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745770286) | v1, void around the map |

## layout

```
.
├── docs/
│   └── BUILD.md                # cook / package / upload workflow
├── tools/                      # shared scripts
│   ├── pmx_to_fbx.py           # convert MMD .pmx to .fbx via Blender + mmd_tools
│   ├── wire_materials.py       # UE Python: wire textures into materials from a json manifest
│   └── *_material_textures.json
├── mods/
│   └── <mod-name>/
│       ├── README.md           # per-mod notes, credits, source
│       ├── Plugins/<Mod>/      # UE plugin source (Content + Resources + .uplugin)
│       └── workshop/<Mod>.vdf  # workshop upload manifest (publishedfileid=0 in repo)
└── LICENSE
```

## adding a new mod

1. New plugin in `MecchaCModKit_Load/Plugins/<ModName>/` (Edit > Plugins > Add > Content Only).
2. Build the level in `Content/Maps/`.
3. Cook + package per [`docs/BUILD.md`](docs/BUILD.md).
4. Copy `Content/`, `Resources/`, and the `.uplugin` into a new `mods/<mod-name>/Plugins/<ModName>/` here. Commit.

## tools

- `tools/pmx_to_fbx.py`: takes a `.pmx` MikuMikuDance model, runs it through Blender + [mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools), spits out a `.fbx` plus a json manifest of which material uses which texture. Useful if your source is MMD. Not used for Windfall (that one used .obj from Models Resource).
- `tools/wire_materials.py`: UE editor Python script. Reads the json manifest and assigns each PNG texture to the matching material's Base Color slot. Handy when UE's importer drops material refs.

## license

MIT. See [LICENSE](LICENSE).

Game assets under `mods/*/Plugins/*/Content/` come from fan rips of game data. Credits are in each mod's README.
