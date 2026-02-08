"""get full scene inventory for docs."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

print("=== MESHES ===")
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == 'MESH':
        p = len(obj.data.polygons)
        t = sum(len(f.vertices)-2 for f in obj.data.polygons)
        m = len(obj.data.materials)
        mat_name = obj.data.materials[0].name if obj.data.materials else "none"
        print(f"  {obj.name}: {p}p {t}t {m}m -> {mat_name}")

print("\n=== LIGHTS ===")
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == 'LIGHT':
        c = tuple(round(v,2) for v in obj.data.color)
        loc = [round(v,1) for v in obj.location]
        print(f"  {obj.name}: e={obj.data.energy} color={c} loc={loc}")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
tp = sum(len(o.data.polygons) for o in meshes)
tt = sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes)
mats = set()
for o in meshes:
    for s in o.material_slots:
        if s.material:
            mats.add(s.material.name)

print(f"\n=== TOTALS ===")
print(f"  meshes: {len(meshes)}")
print(f"  polys: {tp}")
print(f"  tris: {tt}")
print(f"  materials: {len(mats)}")
print(f"  lights: {len([o for o in bpy.data.objects if o.type == 'LIGHT'])}")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
