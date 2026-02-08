"""validate scene against horizon worlds constraints and export fbx."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

# --- step 1: validate ---
VALIDATE = r"""
import bpy

MAX_POLYS = 50000
MAX_MATERIALS = 2
errors = []
report = []

for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue

    polys = len(obj.data.polygons)
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    mats = len(obj.data.materials)

    status = "OK"
    if polys > MAX_POLYS:
        errors.append(f"{obj.name}: {polys} polys exceeds {MAX_POLYS} limit")
        status = "OVER LIMIT"
    if mats > MAX_MATERIALS:
        errors.append(f"{obj.name}: {mats} materials exceeds {MAX_MATERIALS} limit")
        status = "OVER LIMIT"

    report.append(f"{obj.name}: {polys} polys, {tris} tris, {mats} mat(s) — {status}")

    # apply all transforms
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)

print("=== VALIDATION REPORT ===")
for line in report:
    print(line)

if errors:
    print(f"\nFAILED: {len(errors)} error(s)")
    for e in errors:
        print(f"  ERROR: {e}")
else:
    total_polys = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    total_tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    print(f"\nPASSED — {total_polys} total polys, {total_tris} total tris")
    print("transforms applied to all meshes")
"""

print("--- validating scene ---")
result = execute_code(VALIDATE)
print(result.get("result", {}).get("result", result))

# --- step 2: export fbx ---
EXPORT = r"""
import bpy
import os

export_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx"
os.makedirs(export_dir, exist_ok=True)
filepath = os.path.join(export_dir, "pg_origin_club_phase1.fbx")

bpy.ops.export_scene.fbx(
    filepath=filepath,
    use_selection=False,
    apply_scale_options='FBX_SCALE_ALL',
    apply_unit_scale=True,
    bake_space_transform=True,
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
    add_leaf_bones=False,
    path_mode='COPY',
    embed_textures=True,
    object_types={'MESH', 'LIGHT', 'CAMERA'},
)

file_size = os.path.getsize(filepath)
print(f"exported: {filepath}")
print(f"file size: {file_size} bytes ({file_size/1024:.1f} kb)")
"""

print("\n--- exporting fbx ---")
result = execute_code(EXPORT)
print(result.get("result", {}).get("result", result))

# --- step 3: save .blend ---
SAVE = r"""
import bpy
import os

blend_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world"
os.makedirs(blend_dir, exist_ok=True)
filepath = os.path.join(blend_dir, "pg_origin_club.blend")
bpy.ops.wm.save_as_mainfile(filepath=filepath)
print(f"saved: {filepath}")
"""

print("\n--- saving blend file ---")
result = execute_code(SAVE)
print(result.get("result", {}).get("result", result))
