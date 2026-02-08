"""phase 3: final validation and export."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

# --- clean up stale materials ---
CLEANUP = r"""
import bpy

# remove orphan materials not assigned to any object
used_mats = set()
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                used_mats.add(slot.material.name)

removed = []
for mat in list(bpy.data.materials):
    if mat.name not in used_mats:
        removed.append(mat.name)
        bpy.data.materials.remove(mat)

if removed:
    print(f"cleaned up {len(removed)} orphan materials: {removed}")
else:
    print("no orphan materials")
"""

print("--- cleanup ---")
r = execute_code(CLEANUP)
print(r.get("result", {}).get("result", r))

# --- validate ---
VALIDATE = r"""
import bpy

MAX_POLYS = 50000
MAX_MATERIALS = 2
errors = []
report = []

for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type != 'MESH':
        continue

    polys = len(obj.data.polygons)
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    mats = len(obj.data.materials)

    status = "OK"
    if polys > MAX_POLYS:
        errors.append(f"{obj.name}: {polys} polys > {MAX_POLYS}")
        status = "OVER"
    if mats > MAX_MATERIALS:
        errors.append(f"{obj.name}: {mats} materials > {MAX_MATERIALS}")
        status = "OVER"

    report.append(f"  {obj.name}: {polys}p {tris}t {mats}m — {status}")

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)

print("=== FINAL VALIDATION ===")
for line in report:
    print(line)

mesh_count = len([o for o in bpy.data.objects if o.type == 'MESH'])
light_count = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
total_polys = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
total_tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
mat_count = len(bpy.data.materials)

if errors:
    print(f"\nFAILED: {len(errors)} error(s)")
    for e in errors:
        print(f"  ERROR: {e}")
else:
    print(f"\nPASSED")
    print(f"  meshes: {mesh_count}")
    print(f"  lights: {light_count}")
    print(f"  polys: {total_polys}")
    print(f"  tris: {total_tris}")
    print(f"  materials: {mat_count}")
"""

print("\n--- validate ---")
r = execute_code(VALIDATE)
print(r.get("result", {}).get("result", r))

# --- export ---
EXPORT = r"""
import bpy
import os

export_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx"
os.makedirs(export_dir, exist_ok=True)
filepath = os.path.join(export_dir, "pg_origin_club_phase3.fbx")

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

# also export a final named version
final_path = os.path.join(export_dir, "pg_origin_club_final.fbx")
bpy.ops.export_scene.fbx(
    filepath=final_path,
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

size2 = os.path.getsize(final_path)
print(f"exported: {final_path}")
print(f"size: {size2} bytes ({size2/1024:.1f} kb)")
"""

print("\n--- export ---")
r = execute_code(EXPORT)
print(r.get("result", {}).get("result", r))

# --- save .blend ---
SAVE = r"""
import bpy
filepath = "/Users/chanceneihouse/GitHub/world-builder-agent/world/pg_origin_club.blend"
bpy.ops.wm.save_as_mainfile(filepath=filepath)
print(f"saved: {filepath}")
"""

print("\n--- save ---")
r = execute_code(SAVE)
print(r.get("result", {}).get("result", r))
