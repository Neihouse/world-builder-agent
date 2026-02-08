"""phase 2: validate and export."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

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
        errors.append(f"{obj.name}: {polys} polys exceeds {MAX_POLYS}")
        status = "OVER"
    if mats > MAX_MATERIALS:
        errors.append(f"{obj.name}: {mats} materials exceeds {MAX_MATERIALS}")
        status = "OVER"

    report.append(f"{obj.name}: {polys} polys, {tris} tris, {mats} mat — {status}")

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)

print("=== VALIDATION ===")
for line in sorted(report):
    print(line)

total_polys = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
total_tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
mesh_count = len([o for o in bpy.data.objects if o.type == 'MESH'])

if errors:
    print(f"\nFAILED: {len(errors)} error(s)")
    for e in errors:
        print(f"  ERROR: {e}")
else:
    print(f"\nPASSED — {mesh_count} meshes, {total_polys} polys, {total_tris} tris")
"""

EXPORT = r"""
import bpy
import os

export_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx"
os.makedirs(export_dir, exist_ok=True)
filepath = os.path.join(export_dir, "pg_origin_club_phase2.fbx")

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

size = os.path.getsize(filepath)
print(f"exported: {filepath}")
print(f"size: {size} bytes ({size/1024:.1f} kb)")
"""

SAVE = r"""
import bpy
filepath = "/Users/chanceneihouse/GitHub/world-builder-agent/world/pg_origin_club.blend"
bpy.ops.wm.save_as_mainfile(filepath=filepath)
print(f"saved: {filepath}")
"""

print("--- validate ---")
r = execute_code(VALIDATE)
print(r.get("result", {}).get("result", r))

print("\n--- export ---")
r = execute_code(EXPORT)
print(r.get("result", {}).get("result", r))

print("\n--- save blend ---")
r = execute_code(SAVE)
print(r.get("result", {}).get("result", r))
