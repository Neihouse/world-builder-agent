"""phase 3: polish materials for atmosphere depth."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

# === PHASE 3: MATERIAL POLISH ===
# refine existing materials for better depth and atmosphere
# tune roughness/metallic for realistic light interaction
# boost emissive elements slightly for visibility
# add second material to stage platform for edge accent

def get_bsdf(mat):
    return mat.node_tree.nodes.get("Principled BSDF")

# --- floor: slightly warmer, more variation in roughness ---
mat = bpy.data.materials["DarkConcrete_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.055, 0.05, 0.06, 1.0)
bsdf.inputs["Roughness"].default_value = 0.88
bsdf.inputs["Metallic"].default_value = 0.05
# add subtle specular for wet concrete look
bsdf.inputs["IOR"].default_value = 1.45

# --- walls: cooler, absorb more light ---
mat = bpy.data.materials["DarkWall_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.025, 0.025, 0.035, 1.0)
bsdf.inputs["Roughness"].default_value = 0.95

# --- ceiling: near-black, barely visible ---
mat = bpy.data.materials["DarkCeiling_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.015, 0.015, 0.018, 1.0)
bsdf.inputs["Roughness"].default_value = 0.98

# --- stage platform: add slight sheen, warmer ---
mat = bpy.data.materials["StageSurface_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.09, 0.07, 0.1, 1.0)
bsdf.inputs["Roughness"].default_value = 0.5
bsdf.inputs["Metallic"].default_value = 0.4

# --- dj booth: more polished metal ---
mat = bpy.data.materials["BoothMetal_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.035, 0.035, 0.045, 1.0)
bsdf.inputs["Roughness"].default_value = 0.3
bsdf.inputs["Metallic"].default_value = 0.9

# --- backdrop: tune emission for balanced glow ---
mat = bpy.data.materials["Backdrop_Unlit"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.08, 0.04, 0.12, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.12, 0.06, 0.2, 1.0)
bsdf.inputs["Emission Strength"].default_value = 2.5

# --- origin focal: darker, more contrast with ring ---
mat = bpy.data.materials["OriginSurface_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.055, 1.0)
bsdf.inputs["Roughness"].default_value = 0.4
bsdf.inputs["Metallic"].default_value = 0.6

# --- origin ring: stronger glow, more defined ---
mat = bpy.data.materials["OriginRing_Unlit"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.18, 0.1, 0.3, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.2, 0.12, 0.35, 1.0)
bsdf.inputs["Emission Strength"].default_value = 5.0

# --- columns: slightly warmer than walls, catch light better ---
mat = bpy.data.materials["ColumnStone_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.065, 0.055, 0.075, 1.0)
bsdf.inputs["Roughness"].default_value = 0.7
bsdf.inputs["Metallic"].default_value = 0.25

# --- frame: mirror-dark metal ---
mat = bpy.data.materials["FrameMetal_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.03, 0.025, 0.04, 1.0)
bsdf.inputs["Roughness"].default_value = 0.25
bsdf.inputs["Metallic"].default_value = 0.95

# --- relief: boost glow slightly ---
mat = bpy.data.materials["ReliefGlow_Unlit"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.14, 0.07, 0.22, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.16, 0.08, 0.25, 1.0)
bsdf.inputs["Emission Strength"].default_value = 5.0

# --- totems: subtle warm shift from columns ---
mat = bpy.data.materials["TotemStone_Metal"]
bsdf = get_bsdf(mat)
bsdf.inputs["Base Color"].default_value = (0.055, 0.045, 0.065, 1.0)
bsdf.inputs["Roughness"].default_value = 0.55
bsdf.inputs["Metallic"].default_value = 0.45

print("materials polished:")
for mat in sorted(bpy.data.materials, key=lambda m: m.name):
    if mat.use_nodes:
        bsdf = get_bsdf(mat)
        if bsdf:
            r = round(bsdf.inputs["Roughness"].default_value, 2)
            m = round(bsdf.inputs["Metallic"].default_value, 2)
            e = round(bsdf.inputs["Emission Strength"].default_value, 1)
            print(f"  {mat.name}: rough={r} metal={m} emit={e}")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
