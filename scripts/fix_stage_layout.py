"""fix stage layout — move backdrop, relief, frame behind DJ against back wall."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

# === CURRENT LAYOUT (WRONG) ===
# back wall:      y = -7.5
# stage center:   y = -5.2 (spans -7.2 to -3.2)
# dj booth:       y = -6.2 (toward back wall — correct)
# backdrop:       y = -3.5 (FRONT of stage — WRONG, should be behind DJ)
# relief:         on backdrop (also wrong position)
# frame:          y = -3.2 (FRONT — WRONG)
# totems:         y = -3.2 (FRONT — WRONG)
#
# === TARGET LAYOUT ===
# audience → origin (y=0) → open stage → DJ booth (y=-6.2) → backdrop/frame/relief (y~-7.1)
# everything behind the DJ, against the back wall

BACK_Y = -7.1  # just in front of back wall (-7.5)

# --- delete old backdrop, relief, frame, totems ---
to_delete = ["Stage_Backdrop", "Backdrop_Relief", "Stage_Frame", "Totem_L", "Totem_R"]
for name in to_delete:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
        print(f"deleted {name}")

# --- rebuild backdrop at back wall ---
PANEL_W = 8.0
PANEL_H = 3.0
PANEL_T = 0.1
PANEL_Y = BACK_Y
PANEL_Z = 0.6 + PANEL_H / 2  # stage height + half panel

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, PANEL_Y, PANEL_Z))
backdrop = bpy.context.active_object
backdrop.name = "Stage_Backdrop"
backdrop.scale = (PANEL_W, PANEL_T, PANEL_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

mat = bpy.data.materials.get("Backdrop_Unlit")
if mat:
    backdrop.data.materials.clear()
    backdrop.data.materials.append(mat)

# --- rebuild relief on backdrop (in front of it, facing audience) ---
RELIEF_Y = PANEL_Y + 0.08

rings = [
    {"radius": 1.1, "depth": 0.04},
    {"radius": 0.75, "depth": 0.06},
    {"radius": 0.4, "depth": 0.08},
]

ring_names = []
for i, ring in enumerate(rings):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=ring["radius"],
        depth=ring["depth"],
        location=(0, RELIEF_Y, PANEL_Z)
    )
    r = bpy.context.active_object
    r.rotation_euler = (math.pi/2, 0, math.pi/8)
    r.name = f"Relief_Ring_{i}"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ring_names.append(r.name)

# center point
bpy.ops.mesh.primitive_cylinder_add(
    vertices=8, radius=0.15, depth=0.10,
    location=(0, RELIEF_Y + 0.02, PANEL_Z)
)
c = bpy.context.active_object
c.rotation_euler = (math.pi/2, 0, math.pi/8)
c.name = "Relief_Center"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
ring_names.append("Relief_Center")

# radiating bars
bar_length = 1.0
bar_w = 0.025
bar_d = 0.04
for j in range(4):
    angle = j * (math.pi / 4) + math.pi / 8
    dx = math.cos(angle) * bar_length / 2
    dz = math.sin(angle) * bar_length / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(dx, RELIEF_Y, PANEL_Z + dz)
    )
    bar = bpy.context.active_object
    bar.name = f"Relief_Bar_{j}"
    bar.scale = (bar_length, bar_d, bar_w)
    bar.rotation_euler = (0, -angle, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ring_names.append(bar.name)

# join relief
bpy.ops.object.select_all(action='DESELECT')
for name in ring_names:
    obj = bpy.data.objects.get(name)
    if obj:
        obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[ring_names[0]]
bpy.ops.object.join()
relief = bpy.context.active_object
relief.name = "Backdrop_Relief"

mat = bpy.data.materials.get("ReliefGlow_Unlit")
if mat:
    relief.data.materials.clear()
    relief.data.materials.append(mat)

# --- rebuild frame behind DJ, framing the backdrop ---
FRAME_W = 9.0
PILLAR_W = 0.5
PILLAR_D = 0.4
PILLAR_H = 3.8
LINTEL_H = 0.4
FRAME_Y = PANEL_Y + 0.2  # just in front of backdrop

bpy.ops.mesh.primitive_cube_add(size=1, location=(-FRAME_W/2, FRAME_Y, PILLAR_H/2))
pl = bpy.context.active_object
pl.name = "Frame_PL"
pl.scale = (PILLAR_W, PILLAR_D, PILLAR_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

bpy.ops.mesh.primitive_cube_add(size=1, location=(FRAME_W/2, FRAME_Y, PILLAR_H/2))
pr = bpy.context.active_object
pr.name = "Frame_PR"
pr.scale = (PILLAR_W, PILLAR_D, PILLAR_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, FRAME_Y, PILLAR_H + LINTEL_H/2))
li = bpy.context.active_object
li.name = "Frame_LI"
li.scale = (FRAME_W + PILLAR_W, PILLAR_D, LINTEL_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

bpy.ops.object.select_all(action='DESELECT')
for n in ["Frame_PL", "Frame_PR", "Frame_LI"]:
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["Frame_PL"]
bpy.ops.object.join()
frame = bpy.context.active_object
frame.name = "Stage_Frame"

mat = bpy.data.materials.get("FrameMetal_Metal")
if mat:
    frame.data.materials.clear()
    frame.data.materials.append(mat)

# --- rebuild totems flanking the backdrop ---
TOTEM_X = 5.5
TOTEM_Y = PANEL_Y + 0.3

for side, sign in [("L", -1), ("R", 1)]:
    x = sign * TOTEM_X
    parts = []

    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.5, radius2=0.35, depth=1.8, location=(x, TOTEM_Y, 0.9))
    b = bpy.context.active_object
    b.name = f"T_{side}_B"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(b.name)

    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.35, radius2=0.2, depth=1.2, location=(x, TOTEM_Y, 2.4))
    m = bpy.context.active_object
    m.name = f"T_{side}_M"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(m.name)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.3, location=(x, TOTEM_Y, 3.21))
    t = bpy.context.active_object
    t.name = f"T_{side}_T"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(t.name)

    bpy.ops.object.select_all(action='DESELECT')
    for n in parts:
        bpy.data.objects[n].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[parts[0]]
    bpy.ops.object.join()
    totem = bpy.context.active_object
    totem.name = f"Totem_{side}"

    mat = bpy.data.materials.get("TotemStone_Metal")
    if mat:
        totem.data.materials.clear()
        totem.data.materials.append(mat)

# --- report ---
print("\n=== NEW LAYOUT ===")
for name in ["Stage_Platform", "DJ_Booth", "Stage_Backdrop", "Backdrop_Relief", "Stage_Frame", "Totem_L", "Totem_R"]:
    obj = bpy.data.objects.get(name)
    if obj:
        # rough y position from vertices
        ys = [v.co.y + obj.location.y for v in obj.data.vertices]
        print(f"  {name}: y=[{min(ys):.1f} to {max(ys):.1f}], {len(obj.data.polygons)}p")

print("\naudience (y=+7.5) → origin (y=0) → stage (y=-5.2) → DJ (y=-6.2) → backdrop/frame (y=-7.1) → wall (y=-7.5)")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
