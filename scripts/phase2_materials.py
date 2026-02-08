"""phase 2: apply materials to identity pass objects."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

# === PHASE 2 MATERIALS ===
# consistent with dark underground palette
# subtle accent differentiation for identity elements

# 1. columns — dark stone, slightly warmer than walls
mat_column = bpy.data.materials.new(name="ColumnStone_Metal")
mat_column.use_nodes = True
bsdf = mat_column.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.06, 0.05, 0.07, 1.0)
bsdf.inputs["Roughness"].default_value = 0.75
bsdf.inputs["Metallic"].default_value = 0.2

# 2. stage frame — dark metal, polished
mat_frame = bpy.data.materials.new(name="FrameMetal_Metal")
mat_frame.use_nodes = True
bsdf = mat_frame.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.04, 0.03, 0.05, 1.0)
bsdf.inputs["Roughness"].default_value = 0.35
bsdf.inputs["Metallic"].default_value = 0.9

# 3. backdrop relief — subtle emissive accent
mat_relief = bpy.data.materials.new(name="ReliefGlow_Unlit")
mat_relief.use_nodes = True
bsdf = mat_relief.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.12, 0.06, 0.18, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.12, 0.06, 0.18, 1.0)
bsdf.inputs["Emission Strength"].default_value = 4.0

# 4. totems — dark stone with slight metallic sheen
mat_totem = bpy.data.materials.new(name="TotemStone_Metal")
mat_totem.use_nodes = True
bsdf = mat_totem.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.05, 0.04, 0.06, 1.0)
bsdf.inputs["Roughness"].default_value = 0.6
bsdf.inputs["Metallic"].default_value = 0.4

# --- assign ---
assignments = {
    "Columns_Left": mat_column,
    "Columns_Right": mat_column,
    "Stage_Frame": mat_frame,
    "Backdrop_Relief": mat_relief,
    "Totem_L": mat_totem,
    "Totem_R": mat_totem,
}

for obj_name, mat in assignments.items():
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        print(f"{obj_name}: material={mat.name}")
    else:
        print(f"WARNING: {obj_name} not found")

print(f"\ntotal materials in scene: {len(bpy.data.materials)}")
"""

result = execute_code(CODE)
print(json.dumps(result, indent=2))
