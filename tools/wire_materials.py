"""
Wire imported Texture assets into Material Base Color slots, per a JSON manifest
mapping material name -> texture filename.

Usage from UE Python console (Window -> Output Log -> switch Cmd to Python):

  exec(open(r"C:\\MechaCham Maps\\_mmd_convert\\wire_materials.py").read())

By default it uses the Windfall manifest. To target a different one, set the
global MANIFEST_OVERRIDE before exec, e.g.:

  MANIFEST_OVERRIDE = r"C:\\MechaCham Maps\\_mmd_convert\\grovestreet_material_textures.json"
  exec(open(r"C:\\MechaCham Maps\\_mmd_convert\\wire_materials.py").read())
"""
import unreal
import json
import os

DEFAULT_MANIFEST = r"C:\MechaCham Maps\_mmd_convert\material_textures.json"
MANIFEST = globals().get("MANIFEST_OVERRIDE", DEFAULT_MANIFEST)
print(f"Using manifest: {MANIFEST}")

with open(MANIFEST, "r", encoding="utf-8") as f:
    mat_to_tex = json.load(f)

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
asset_reg.search_all_assets(True)

MATERIAL_CLASS = unreal.TopLevelAssetPath("/Script/Engine", "Material")
TEXTURE_CLASS  = unreal.TopLevelAssetPath("/Script/Engine", "Texture2D")

# Pre-index all Materials + Textures by name to avoid re-scanning per lookup
print("Indexing materials and textures...")
_mat_index = {}
for a in asset_reg.get_assets_by_class(MATERIAL_CLASS, search_sub_classes=True):
    _mat_index[str(a.asset_name)] = a
_tex_index = {}
for a in asset_reg.get_assets_by_class(TEXTURE_CLASS, search_sub_classes=True):
    _tex_index[str(a.asset_name)] = a
print(f"  {len(_mat_index)} materials, {len(_tex_index)} textures indexed")

def find_asset(name, kind):
    if kind == "material":
        return _mat_index.get(name)
    if kind == "texture":
        return _tex_index.get(name)
    return None

mat_lib = unreal.MaterialEditingLibrary

ok, fail, skip = 0, 0, 0
for mat_name, tex_filename in mat_to_tex.items():
    if not tex_filename:
        skip += 1
        continue
    tex_basename = os.path.splitext(tex_filename)[0]

    mat_asset = find_asset(mat_name, "material")
    tex_asset = find_asset(tex_basename, "texture")

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

    ts = mat_lib.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -400, 0)
    ts.texture = tex
    mat_lib.connect_material_property(ts, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
    mat_lib.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(str(mat_asset.package_name))
    print(f"  [OK]   {mat_name} <- {tex_basename}")
    ok += 1

print(f"\nDone. ok={ok} fail={fail} skip={skip}")
