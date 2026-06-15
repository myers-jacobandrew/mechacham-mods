# mechacham-mods

Custom maps for [Meccha Chameleon](https://store.steampowered.com/), packaged via the MecchaChameleon Custom Mod Kit and published to Steam Workshop.

## Mods

| Mod | Workshop | Status |
|---|---|---|
| [Windfall Island](mods/windfall-island/) | [Workshop link](https://steamcommunity.com/sharedfiles/filedetails/?id=3745643656) | v1 — windmill missing, see notes |

## Repo layout

```
.
├── docs/                       # general build / cook / upload workflow
│   └── BUILD.md
├── tools/                      # shared conversion tooling
│   ├── pmx_to_fbx.py           # PMX (MikuMikuDance) -> FBX via Blender + mmd_tools
│   ├── wire_materials.py       # UE Python script: bulk-wire textures into materials
│   └── *_material_textures.json # per-mod material -> texture manifests
├── mods/
│   └── <mod-name>/
│       ├── README.md           # mod-specific notes / known issues
│       ├── Plugins/<Mod>/      # UE plugin source (Content + Resources + .uplugin)
│       └── workshop/<Mod>.vdf  # Steam Workshop upload manifest (committed with publishedfileid=0)
└── LICENSE                     # MIT
```

## Adding a new mod

1. Make a UE plugin under `MecchaCModKit_Load/Plugins/<ModName>/` (Edit → Plugins → Add → Content Only).
2. Build the level inside the plugin's `Content/Maps/`.
3. When ready, cook + package per `docs/BUILD.md`.
4. Copy the plugin source (`Content/`, `Resources/`, `*.uplugin`) into a new `mods/<mod-name>/Plugins/<ModName>/` here, commit.

## Tooling

- `tools/pmx_to_fbx.py` — converts a `.pmx` MikuMikuDance model to `.fbx` with sibling textures and a `material_textures.json` manifest. Requires Blender 5.0+ with [mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools).
- `tools/wire_materials.py` — UE editor Python script. After bulk-importing the PNGs, this script reads the manifest and assigns each texture to its material's Base Color slot. Works around UE's FBX importer dropping most texture references from mmd_tools-produced FBX.

See `docs/BUILD.md` for the full pipeline.

## License

MIT (see [LICENSE](LICENSE)).

Game assets in `mods/*/Plugins/*/Content/` are derived from third-party fan rips of original game data and are credited per-mod in each mod's README.
