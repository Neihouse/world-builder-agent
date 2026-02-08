"""clean up duplicate objects from rebuild."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

# remove .001 duplicates and stale objects
to_remove = []
for o in bpy.data.objects:
    if ".001" in o.name:
        to_remove.append(o.name)

# also remove old "Ceiling" and "Wall_Front" if they exist alongside new ones
for name in ["Ceiling", "Wall_Front"]:
    if bpy.data.objects.get(name):
        to_remove.append(name)

for name in to_remove:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
        print(f"removed: {name}")

meshes = [o for o in bpy.data.objects if o.type == "MESH"]
tp = sum(len(o.data.polygons) for o in meshes)
tt = sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes)
print(f"\nclean: {len(meshes)} meshes, {tp} polys, {tt} tris")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
