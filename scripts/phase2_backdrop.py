"""phase 2: add concentric geometric relief on the stage backdrop."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

# === BACKDROP RELIEF ===
# concentric octagonal rings radiating from center of backdrop
# primordial/organic feel — like ripples or sound waves
# layered slightly in front of the backdrop panel

# backdrop is at: x=0, y=-3.5, z=1.85, size=5.5w x 2.5h
BACKDROP_Y = -3.5
BACKDROP_Z = 1.85  # center height = stage_h(0.6) + panel_h(2.5)/2
RELIEF_Y = BACKDROP_Y - 0.06  # just in front of backdrop

# concentric octagons — 3 rings, decreasing size
rings = [
    {"radius": 1.1, "thickness": 0.08, "depth": 0.04},
    {"radius": 0.75, "thickness": 0.06, "depth": 0.06},
    {"radius": 0.4, "thickness": 0.05, "depth": 0.08},
]

ring_names = []
for i, ring in enumerate(rings):
    # outer octagon
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=ring["radius"],
        depth=ring["depth"],
        location=(0, RELIEF_Y, BACKDROP_Z)
    )
    outer = bpy.context.active_object
    outer.rotation_euler = (math.pi/2, 0, math.pi/8)  # face forward, rotate 22.5deg
    outer.name = f"Relief_Ring_{i}"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ring_names.append(outer.name)

# center point — small octagonal solid
bpy.ops.mesh.primitive_cylinder_add(
    vertices=8,
    radius=0.15,
    depth=0.10,
    location=(0, RELIEF_Y - 0.02, BACKDROP_Z)
)
center = bpy.context.active_object
center.rotation_euler = (math.pi/2, 0, math.pi/8)
center.name = "Relief_Center"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
ring_names.append("Relief_Center")

# radiating lines — 4 diagonal bars emanating from center
for j in range(4):
    angle = math.pi/4 * j + math.pi/8  # 22.5deg offset
    length = 1.0
    cx = math.cos(angle) * length / 2
    cz = math.sin(angle) * length / 2 + BACKDROP_Z

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, RELIEF_Y - 0.01, cz))
    bar = bpy.context.active_object
    bar.scale = (0.03, 0.03, length)
    bar.rotation_euler = (0, angle, 0)  # rotate in xz plane
    # need to rotate to face the wall plane
    bar.rotation_euler = (0, 0, angle)
    bar.scale = (length, 0.03, 0.03)
    bar.rotation_euler = (math.pi/2, 0, angle)
    # simpler: just position along xz plane
    pass

    # actually let's keep it simple — position manually
    bpy.data.objects.remove(bar, do_unlink=True)

# simpler radiating lines — horizontal and vertical bars on the backdrop face
bar_length = 1.0
bar_w = 0.025
bar_d = 0.04
bars_created = []

# 4 radiating bars at 45-degree intervals
for j in range(4):
    angle = j * (math.pi / 4) + math.pi / 8
    dx = math.cos(angle) * bar_length / 2
    dz = math.sin(angle) * bar_length / 2

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(dx, RELIEF_Y, BACKDROP_Z + dz)
    )
    bar = bpy.context.active_object
    bar.name = f"Relief_Bar_{j}"

    # scale and rotate to align with angle
    bar.scale = (bar_length, bar_d, bar_w)
    bar.rotation_euler = (0, 0, 0)

    # rotate around y axis (which is depth axis since bar faces camera)
    # actually we want rotation in the xz plane viewed from y
    # the bar lies along x by default, rotate around y to fan out
    import mathutils
    bar.rotation_euler = (0, -angle, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bars_created.append(bar.name)

ring_names.extend(bars_created)

# join all relief pieces
bpy.ops.object.select_all(action='DESELECT')
for name in ring_names:
    obj = bpy.data.objects.get(name)
    if obj:
        obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[ring_names[0]]
bpy.ops.object.join()
relief = bpy.context.active_object
relief.name = "Backdrop_Relief"

polys = len(relief.data.polygons)
print(f"Backdrop_Relief: {polys} polys")
"""

result = execute_code(CODE)
print(json.dumps(result, indent=2))
