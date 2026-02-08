"""restore materials and lighting to pre-darken state."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

def get_bsdf(mat):
    return mat.node_tree.nodes.get("Principled BSDF")

# === RESTORE ALL MATERIALS TO PHASE 3 POLISH VALUES ===

mats = {
    "DarkConcrete_Metal": {"base": (0.055, 0.05, 0.06, 1), "rough": 0.88, "metal": 0.05, "ior": 1.45, "emit": 0},
    "DarkWall_Metal": {"base": (0.025, 0.025, 0.035, 1), "rough": 0.95, "metal": 0.0, "emit": 0},
    "DarkCeiling_Metal": {"base": (0.015, 0.015, 0.018, 1), "rough": 0.98, "metal": 0.0, "emit": 0},
    "StageSurface_Metal": {"base": (0.09, 0.07, 0.1, 1), "rough": 0.5, "metal": 0.4, "emit": 0},
    "BoothMetal_Metal": {"base": (0.035, 0.035, 0.045, 1), "rough": 0.3, "metal": 0.9, "emit": 0},
    "Backdrop_Unlit": {"base": (0.08, 0.04, 0.12, 1), "emit_color": (0.12, 0.06, 0.2, 1), "emit": 2.5, "rough": 0.5, "metal": 0.0},
    "OriginSurface_Metal": {"base": (0.04, 0.04, 0.055, 1), "rough": 0.4, "metal": 0.6, "emit": 0},
    "OriginRing_Unlit": {"base": (0.18, 0.1, 0.3, 1), "emit_color": (0.2, 0.12, 0.35, 1), "emit": 5.0, "rough": 0.5, "metal": 0.0},
    "ColumnStone_Metal": {"base": (0.065, 0.055, 0.075, 1), "rough": 0.7, "metal": 0.25, "emit": 0},
    "FrameMetal_Metal": {"base": (0.03, 0.025, 0.04, 1), "rough": 0.25, "metal": 0.95, "emit": 0},
    "ReliefGlow_Unlit": {"base": (0.14, 0.07, 0.22, 1), "emit_color": (0.16, 0.08, 0.25, 1), "emit": 5.0, "rough": 0.5, "metal": 0.0},
    "TotemStone_Metal": {"base": (0.055, 0.045, 0.065, 1), "rough": 0.55, "metal": 0.45, "emit": 0},
    "FlowGuide_Unlit": {"base": (0.08, 0.06, 0.12, 1), "emit_color": (0.1, 0.07, 0.16, 1), "emit": 2.0, "rough": 0.5, "metal": 0.0},
    "BeamConcrete_Metal": {"base": (0.035, 0.035, 0.04, 1), "rough": 0.85, "metal": 0.1, "emit": 0},
}

for name, cfg in mats.items():
    mat = bpy.data.materials.get(name)
    if not mat:
        continue
    bsdf = get_bsdf(mat)
    if not bsdf:
        continue
    bsdf.inputs["Base Color"].default_value = cfg["base"]
    bsdf.inputs["Roughness"].default_value = cfg["rough"]
    bsdf.inputs["Metallic"].default_value = cfg["metal"]
    bsdf.inputs["Emission Strength"].default_value = cfg["emit"]
    if "emit_color" in cfg:
        bsdf.inputs["Emission Color"].default_value = cfg["emit_color"]
    if "ior" in cfg:
        bsdf.inputs["IOR"].default_value = cfg["ior"]

# === RESTORE LIGHTING ===
lights = {
    "Light_Stage":     {"energy": 800, "color": (1.0, 0.8, 0.6), "size": 0.8, "loc": (0, -5.2, 3.6)},
    "Light_Origin":    {"energy": 400, "color": (0.5, 0.6, 1.0), "size": 1.5, "loc": (0, 0, 3.5)},
    "Light_Fill":      {"energy": 60,  "color": (0.4, 0.35, 0.5), "size": 6.0, "loc": (0, 5.0, 2.0)},
    "Light_Left":      {"energy": 200, "color": (0.6, 0.25, 0.9), "size": 1.8, "loc": (-7.0, -1.0, 2.8)},
    "Light_Right":     {"energy": 200, "color": (0.6, 0.25, 0.9), "size": 1.8, "loc": (7.0, -1.0, 2.8)},
    "Light_ColWash_L": {"energy": 80,  "color": (0.9, 0.6, 0.4), "size": 3.0, "loc": (-9.0, 0, 1.0)},
    "Light_ColWash_R": {"energy": 80,  "color": (0.9, 0.6, 0.4), "size": 3.0, "loc": (9.0, 0, 1.0)},
    "Light_StageBack": {"energy": 120, "color": (0.3, 0.15, 0.5), "size": 2.0, "loc": (0, -6.8, 1.5)},
}

for name, cfg in lights.items():
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != "LIGHT":
        continue
    obj.data.energy = cfg["energy"]
    obj.data.color = cfg["color"]
    obj.data.shadow_soft_size = cfg["size"]
    obj.location = cfg["loc"]

# restore world background
scene = bpy.context.scene
if scene.world and scene.world.use_nodes:
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.005, 0.005, 0.008, 1.0)
        bg.inputs["Strength"].default_value = 0.1

print("restored all materials and lighting to phase 3 values")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
