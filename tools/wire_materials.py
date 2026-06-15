"""
Run this inside Unreal Editor's Python console (Window -> Output Log -> Cmd drop -> Python).

Or: paste into the Cmd field at the bottom and switch to Python mode.

Assumes:
  - Materials Material0..Material31 exist somewhere in /Game (or under your Plugins)
  - Textures named like 'gakkou03', 'rotennuno4', etc. (matching the PNG basenames) exist in /Game
"""
import unreal
import json
import os

MANIFEST = r"C:\MechaCham Maps\_mmd_convert\material_textures.json"

with open(MANIFEST, "r", encoding="utf-8") as f:
    mat_to_tex = json.load(f)

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
asset_reg.search_all_assets(True)

# Build name -> asset path index
def find_asset(name, class_path):
    """Return first AssetData whose object_name == name."""
    results = asset_reg.get_assets_by_class(class_path, search_sub_classes=True)
    for a in results:
        if str(a.asset_name) == name:
            return a
    return None

mat_lib = unreal.MaterialEditingLibrary

ok, fail, skip = 0, 0, 0
for mat_name, tex_filename in mat_to_tex.items():
    if not tex_filename:
        skip += 1
        continue
    tex_basename = os.path.splitext(tex_filename)[0]

    mat_asset = find_asset(mat_name, "/Script/Engine.Material")
    tex_asset = find_asset(tex_basename, "/Script/Engine.Texture2D")

    if not mat_asset:
        print(f"  [MISS] material not found: {mat_name}")
        fail += 1
        continue
    if not tex_asset:
        print(f"  [MISS] texture not found:  {tex_basename}")
        fail += 1
        continue

    mat = unreal.load_asset(str(mat_asset.package_name) + "." + str(mat_asset.asset_name))
    tex = unreal.load_asset(str(tex_asset.package_name) + "." + str(tex_asset.asset_name))

    # Clear existing expressions for that material's base color, then add texture sample
    # Simpler: just create a TextureSample node and wire to Base Color
    ts = mat_lib.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -400, 0)
    ts.texture = tex
    mat_lib.connect_material_property(ts, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
    mat_lib.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(str(mat_asset.package_name))
    print(f"  [OK]   {mat_name} <- {tex_basename}")
    ok += 1

print(f"\nDone. ok={ok} fail={fail} skip={skip}")
