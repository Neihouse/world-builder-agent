"""phase 3: refine lighting for underground club atmosphere."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

# === PHASE 3: LIGHTING REFINEMENT ===
# goals:
#   - deepen underground mood
#   - warm/cool contrast between stage and crowd area
#   - column wash for rhythm visibility
#   - subtle floor edge glow
#   - no complex rigs, keep under 10 total lights

W = 20.0
D = 15.0
H = 4.0

# --- rework existing lights ---

# stage light — tighter, warmer, stronger
light = bpy.data.objects["Light_Stage"]
light.location = (0, -5.2, 3.6)
light.data.energy = 800
light.data.color = (1.0, 0.8, 0.6)
light.data.shadow_soft_size = 0.8

# origin light — cooler, tighter focus
light = bpy.data.objects["Light_Origin"]
light.location = (0, 0, 3.5)
light.data.energy = 400
light.data.color = (0.5, 0.6, 1.0)
light.data.shadow_soft_size = 1.5

# fill — much dimmer, acts as ambient floor wash
light = bpy.data.objects["Light_Fill"]
light.location = (0, 5.0, 2.0)
light.data.energy = 60
light.data.color = (0.4, 0.35, 0.5)
light.data.shadow_soft_size = 6.0

# left accent — pull in tighter, deeper purple
light = bpy.data.objects["Light_Left"]
light.location = (-7.0, -1.0, 2.8)
light.data.energy = 200
light.data.color = (0.6, 0.25, 0.9)
light.data.shadow_soft_size = 1.8

# right accent — mirror
light = bpy.data.objects["Light_Right"]
light.location = (7.0, -1.0, 2.8)
light.data.energy = 200
light.data.color = (0.6, 0.25, 0.9)
light.data.shadow_soft_size = 1.8

# --- add new accent lights ---

# column wash left — low warm light grazing columns
bpy.ops.object.light_add(type='POINT', location=(-9.0, 0, 1.0))
col_wash_l = bpy.context.active_object
col_wash_l.name = "Light_ColWash_L"
col_wash_l.data.energy = 80
col_wash_l.data.color = (0.9, 0.6, 0.4)
col_wash_l.data.shadow_soft_size = 3.0

# column wash right
bpy.ops.object.light_add(type='POINT', location=(9.0, 0, 1.0))
col_wash_r = bpy.context.active_object
col_wash_r.name = "Light_ColWash_R"
col_wash_r.data.energy = 80
col_wash_r.data.color = (0.9, 0.6, 0.4)
col_wash_r.data.shadow_soft_size = 3.0

# stage backlight — low behind backdrop, creates silhouette depth
bpy.ops.object.light_add(type='POINT', location=(0, -6.8, 1.5))
backlight = bpy.context.active_object
backlight.name = "Light_StageBack"
backlight.data.energy = 120
backlight.data.color = (0.3, 0.15, 0.5)
backlight.data.shadow_soft_size = 2.0

# report
lights = [o for o in bpy.data.objects if o.type == "LIGHT"]
print(f"total lights: {len(lights)}")
for l in sorted(lights, key=lambda o: o.name):
    loc = [round(c, 1) for c in l.location]
    print(f"  {l.name}: e={l.data.energy} c={tuple(round(c,2) for c in l.data.color)} loc={loc}")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
