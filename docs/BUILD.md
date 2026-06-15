# Build / Cook / Upload workflow

The general pipeline for shipping a custom map to Steam Workshop.

## Prerequisites

- UE 5.6.1 with MecchaChameleon Custom Mod Kit project (`MecchaCModKit_Load`)
- Plugin folder created under `MecchaCModKit_Load/Plugins/<ModName>/` (Content Only)
- Level inside the plugin (with World Partition + Streaming OFF)
- Player spawn at world (0, 0, 100)
- Camera collision profile set to `CameraBlockWall` on relevant geometry
- SteamCmd installed (e.g. `C:\Steamworkshop\SteamCmd\steamcmd.exe`)

## 1. Profile setup (Legacy Project Launcher)

Two profiles are needed: **FullGame** (creates a 1.0 release of the base game) and **<ModName>** (cooks the plugin against that release).

### FullGame profile

| Field | Value |
|---|---|
| Project | `MecchaCModKit_Load` |
| Build | Enabled (Development) |
| Cook | By the Book |
| Cooked Platforms | Windows |
| Cooked Cultures | `en` only |
| Cooked Maps | (empty — cook all) |
| **Release/DLC → Create a release version** | ✅ |
| **Name of the new release to create** | `1.0` |
| Release version this is based on | (empty) |
| Build DLC | ☐ |
| Package | Do not package |
| Deploy | Do not deploy |

### <ModName> profile

| Field | Value |
|---|---|
| Project | `MecchaCModKit_Load` |
| Build | Skip (already built) |
| Cook | By the Book |
| Cooked Platforms | Windows |
| Cooked Cultures | `en` |
| **Release/DLC → Build DLC** | ✅ |
| **Name of the DLC to build** | `<ModName>` (must match plugin folder name **exactly**) |
| **Release version this is based on** | `1.0` |
| Include engine content | ✅ |
| Package | Do not package |
| Deploy | Do not deploy |

## 2. Run the cooks

Run **FullGame first**, then **<ModName>**. The DLC cook fails if FullGame hasn't created the 1.0 release.

If you hit `UnauthorizedAccessException` to `C:\Program Files\Epic Games\UE_5.6\Engine\Programs\AutomationTool\Saved` — launch UE as **Administrator** once to grant write access to that folder.

### Verify release output

After FullGame, this should exist:
```
MecchaCModKit_Load/Releases/1.0/Windows/Metadata/AssetRegistry.bin
```

If not, the FullGame profile is misconfigured (most common: `1.0` is in "based on" field instead of "name of new release").

### Verify DLC output

After <ModName>, these should exist:
```
MecchaCModKit_Load/Plugins/<ModName>/Saved/StagedBuilds/Windows/MecchaCModKit_Load/Plugins/<ModName>/Content/Paks/Windows/
  ├── <ModName>MecchaCModKit_Load-Windows.pak
  ├── <ModName>MecchaCModKit_Load-Windows.ucas
  └── <ModName>MecchaCModKit_Load-Windows.utoc

MecchaCModKit_Load/Plugins/<ModName>/Saved/Cooked/Windows/MecchaCModKit_Load/Plugins/<ModName>/
  └── AssetRegistry.bin
```

## 3. Assemble Workshop bundle

Make a folder `C:\Steamworkshop\<ModName>\` containing:
- The 3 cook files (`.pak`, `.ucas`, `.utoc`)
- `AssetRegistry.bin`
- `Preview.png` — Workshop thumbnail (768×768 recommended, **must be under 1MB**)
- `<ModName>.vdf` — Workshop upload manifest (see `workshop/Windfall.vdf` as a template)

VDF fields:
- `appid`: `4704690` (Meccha Chameleon — never change)
- `publishedfileid`: `0` for first upload (SteamCmd fills it in after success)
- `contentfolder`: the workshop bundle folder
- `previewfile`: path to Preview.png
- `visibility`: `2` (hidden) recommended for first upload; flip to `0` (public) on Workshop after testing
- `title`, `description`, `changenote`: as desired

## 4. Upload

```powershell
& "C:\Steamworkshop\SteamCmd\steamcmd.exe"
```

At the `Steam>` prompt:
```
login <your_steam_username>
workshop_build_item "C:\Steamworkshop\<ModName>\<ModName>.vdf"
```

On success, SteamCmd writes the new `publishedfileid` back into the vdf. Subscribe to your own mod in-game to verify it loads.

## Gotchas

- **Cook fails with "Access denied"**: launch UE as Admin once, or grant `Users` write permission on `<UE>\Engine\Programs\AutomationTool\Saved`.
- **DLC cook fails with "Require based on release version"**: FullGame didn't create release 1.0. Check the FullGame profile's Release/DLC section — `1.0` belongs in **Name of the new release to create**, not in "based on".
- **Upload fails / no error visible**: Preview.png is too large. Keep under 1MB.
- **Mod loads but is invisible in game**: DLC name in the cook profile must match the plugin folder name exactly (case-sensitive, no spaces).
