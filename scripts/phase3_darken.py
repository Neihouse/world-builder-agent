"""darken materials and lighting — underground club mood."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

def get_bsdf(mat):
    return mat.node_tree.nodes.get("Principled BSDF")

# === DARKEN ALL BASE COLORS ===
# multiply all non-emissive base colors by 0.4 (60% darker)
# pull emissive materials down significantly

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    bsdf = get_bsdf(mat)
    if not bsdf:
        continue

    bc = list(bsdf.inputs["Base Color"].default_value)
    em = bsdf.inputs["Emission Strength"].default_value

    if em > 0:
        # emissive materials — reduce emission, darken base
        bsdf.inputs["Base Color"].default_value = (bc[0]*0.5, bc[1]*0.5, bc[2]*0.5, bc[3])
        bsdf.inputs["Emission Strength"].default_value = em * 0.4
        ec = list(bsdf.inputs["Emission Color"].default_value)
        bsdf.inputs["Emission Color"].default_value = (ec[0]*0.6, ec[1]*0.6, ec[2]*0.6, ec[3])
    else:
        # solid materials — darken base color
        bsdf.inputs["Base Color"].default_value = (bc[0]*0.4, bc[1]*0.4, bc[2]*0.4, bc[3])

# === REWORK LIGHTING — MUCH DARKER ===
# cut all energies drastically, tighten falloff

light_settings = {
    "Light_Stage":     {"energy": 250, "color": (1.0, 0.75, 0.5),  "size": 0.5},
    "Light_Origin":    {"energy": 120, "color": (0.4, 0.5, 1.0),   "size": 1.0},
    "Light_Fill":      {"energy": 15,  "color": (0.3, 0.25, 0.4),  "size": 5.0},
    "Light_Left":      {"energy": 60,  "color": (0.5, 0.15, 0.85), "size": 1.5},
    "Light_Right":     {"energy": 60,  "color": (0.5, 0.15, 0.85), "size": 1.5},
    "Light_ColWash_L": {"energy": 25,  "color": (0.8, 0.5, 0.3),   "size": 2.5},
    "Light_ColWash_R": {"energy": 25,  "color": (0.8, 0.5, 0.3),   "size": 2.5},
    "Light_StageBack": {"energy": 40,  "color": (0.2, 0.1, 0.4),   "size": 1.5},
}

for name, cfg in light_settings.items():
    obj = bpy.data.objects.get(name)
    if obj and obj.type == "LIGHT":
        obj.data.energy = cfg["energy"]
        obj.data.color = cfg["color"]
        obj.data.shadow_soft_size = cfg["size"]

# darken world background to near-black
scene = bpy.context.scene
if scene.world and scene.world.use_nodes:
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.001, 0.001, 0.002, 1.0)
        bg.inputs["Strength"].default_value = 0.02

# report
print("darkened materials:")
for mat in sorted(bpy.data.materials, key=lambda m: m.name):
    if not mat.use_nodes:
        continue
    bsdf = get_bsdf(mat)
    if bsdf:
        bc = tuple(round(c, 3) for c in bsdf.inputs["Base Color"].default_value[:3])
        em = round(bsdf.inputs["Emission Strength"].default_value, 2)
        print(f"  {mat.name}: base={bc} emit={em}")

print("\nlights:")
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == "LIGHT":
        print(f"  {obj.name}: e={obj.data.energy}")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
