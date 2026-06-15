"""
PMX -> FBX via Blender + mmd_tools.
v2: Don't embed textures. Copy them next to FBX. Also dump material->texture
manifest as JSON so UE can wire them up afterwards.
"""
import bpy
import os
import sys
import json
import shutil
import addon_utils

PMX_PATH = r"C:\MechaCham Maps\Windfall Island by JuleHyrule\windfall island.pmx"
OUT_DIR  = r"C:\MechaCham Maps\_mmd_convert\out"
FBX_PATH = os.path.join(OUT_DIR, "windfall_island.fbx")
JSON_PATH = os.path.join(OUT_DIR, "material_textures.json")

# Clean and prep output dir
if os.path.isdir(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("Enabling mmd_tools...")
print("=" * 60)
addon_utils.enable("bl_ext.user_default.mmd_tools")

print("Clearing default scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("=" * 60)
print(f"Importing PMX: {PMX_PATH}")
print("=" * 60)
bpy.ops.mmd_tools.import_model(
    filepath=PMX_PATH,
    types={'MESH', 'ARMATURE', 'MORPHS'},
    scale=0.08,
    clean_model=True,
    log_level='INFO'
)

# Walk through all materials and find texture references
print("=" * 60)
print("Material -> texture mapping:")
print("=" * 60)
material_map = {}
src_dir = os.path.dirname(PMX_PATH)
for mat in bpy.data.materials:
    tex_filename = None
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image is not None:
                img = node.image
                # Original filepath may be absolute or relative
                fp = bpy.path.abspath(img.filepath)
                if fp:
                    tex_filename = os.path.basename(fp)
                    break
    material_map[mat.name] = tex_filename
    print(f"  {mat.name:30s} -> {tex_filename}")

# Copy referenced PNGs next to the FBX so UE can find them
print("=" * 60)
print("Copying referenced textures next to FBX...")
print("=" * 60)
copied = set()
for tex in material_map.values():
    if tex and tex not in copied:
        src = os.path.join(src_dir, tex)
        dst = os.path.join(OUT_DIR, tex)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied.add(tex)
            print(f"  copied {tex}")
        else:
            print(f"  MISSING source: {src}")

# Save JSON manifest
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(material_map, f, indent=2, ensure_ascii=False)
print(f"Wrote manifest: {JSON_PATH}")

print("=" * 60)
print(f"Exporting FBX: {FBX_PATH}")
print("=" * 60)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(
    filepath=FBX_PATH,
    use_selection=False,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_ALL',
    object_types={'MESH', 'ARMATURE'},
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
    add_leaf_bones=False,
    bake_anim=False,
    path_mode='STRIP',          # use plain filenames, no paths
    embed_textures=False         # leave textures as external PNGs
)

print("=" * 60)
print(f"DONE. Output: {FBX_PATH}")
print("=" * 60)

if os.path.exists(FBX_PATH):
    size_mb = os.path.getsize(FBX_PATH) / (1024 * 1024)
    print(f"FBX file size: {size_mb:.2f} MB")
    print(f"Textures copied: {len(copied)}")
else:
    print("ERROR: FBX not created!")
    sys.exit(1)
