"""
OBJ -> FBX via Blender. Joins all imported objects into one mesh so UE's
importer doesn't choke on duplicate group IDs.

Run with: blender --background --python obj_to_fbx.py
"""
import bpy
import os
import sys
import json

OBJ_PATH  = r"C:\MechaCham Maps\_mod_imports\GroveStreet\GroveStreet.obj"
OUT_DIR   = r"C:\MechaCham Maps\_mod_imports\GroveStreet\fbx_out"
FBX_PATH  = os.path.join(OUT_DIR, "GroveStreet.fbx")
JSON_PATH = os.path.join(OUT_DIR, "material_textures.json")

os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("Clearing default scene...")
print("=" * 60)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.meshes):
    bpy.data.meshes.remove(block)
for block in list(bpy.data.materials):
    bpy.data.materials.remove(block)

print(f"Importing OBJ: {OBJ_PATH}")
print("=" * 60)
bpy.ops.wm.obj_import(filepath=OBJ_PATH)

mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
print(f"Imported {len(mesh_objs)} mesh objects.")

print("=" * 60)
print("Joining all meshes into one...")
print("=" * 60)
if mesh_objs:
    bpy.ops.object.select_all(action='DESELECT')
    for o in mesh_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = "GroveStreet"
    print(f"Joined mesh: {joined.name}")
    print(f"  vertices: {len(joined.data.vertices)}")
    print(f"  polygons: {len(joined.data.polygons)}")
    print(f"  material slots: {len(joined.material_slots)}")

print("=" * 60)
print("Dumping material -> texture manifest...")
print("=" * 60)
mat_map = {}
src_dir = os.path.dirname(OBJ_PATH)
for mat in bpy.data.materials:
    tex_filename = None
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image is not None:
                fp = bpy.path.abspath(node.image.filepath)
                if fp:
                    tex_filename = os.path.basename(fp)
                    break
    mat_map[mat.name] = tex_filename
print(f"Materials in scene: {len(mat_map)}")
with open(JSON_PATH, "w") as f:
    json.dump(mat_map, f, indent=2)
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
    object_types={'MESH'},
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
    add_leaf_bones=False,
    bake_anim=False,
    path_mode='STRIP',
    embed_textures=False
)

if os.path.exists(FBX_PATH):
    size_mb = os.path.getsize(FBX_PATH) / (1024 * 1024)
    print(f"DONE. FBX size: {size_mb:.2f} MB")
else:
    print("ERROR: FBX not created!")
    sys.exit(1)
