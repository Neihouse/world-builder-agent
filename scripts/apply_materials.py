"""apply horizon-compatible materials to all club objects."""
from blender_cmd import execute_code

CODE = r"""
import bpy

# --- create materials ---

# 1. dark concrete floor
mat_floor = bpy.data.materials.new(name="DarkConcrete_Metal")
mat_floor.use_nodes = True
bsdf = mat_floor.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1.0)
bsdf.inputs["Roughness"].default_value = 0.85
bsdf.inputs["Metallic"].default_value = 0.1

# 2. dark wall
mat_wall = bpy.data.materials.new(name="DarkWall_Metal")
mat_wall.use_nodes = True
bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.03, 0.03, 0.04, 1.0)
bsdf.inputs["Roughness"].default_value = 0.9
bsdf.inputs["Metallic"].default_value = 0.0

# 3. ceiling
mat_ceiling = bpy.data.materials.new(name="DarkCeiling_Metal")
mat_ceiling.use_nodes = True
bsdf = mat_ceiling.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
bsdf.inputs["Roughness"].default_value = 0.95
bsdf.inputs["Metallic"].default_value = 0.0

# 4. stage platform
mat_stage = bpy.data.materials.new(name="StageSurface_Metal")
mat_stage.use_nodes = True
bsdf = mat_stage.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.08, 0.07, 0.09, 1.0)
bsdf.inputs["Roughness"].default_value = 0.6
bsdf.inputs["Metallic"].default_value = 0.3

# 5. dj booth
mat_booth = bpy.data.materials.new(name="BoothMetal_Metal")
mat_booth.use_nodes = True
bsdf = mat_booth.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.05, 1.0)
bsdf.inputs["Roughness"].default_value = 0.4
bsdf.inputs["Metallic"].default_value = 0.8

# 6. backdrop
mat_backdrop = bpy.data.materials.new(name="Backdrop_Unlit")
mat_backdrop.use_nodes = True
bsdf = mat_backdrop.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.1, 0.05, 0.15, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.1, 0.05, 0.15, 1.0)
bsdf.inputs["Emission Strength"].default_value = 2.0

# 7. origin focal
mat_origin = bpy.data.materials.new(name="OriginSurface_Metal")
mat_origin.use_nodes = True
bsdf = mat_origin.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.06, 0.06, 0.08, 1.0)
bsdf.inputs["Roughness"].default_value = 0.5
bsdf.inputs["Metallic"].default_value = 0.5

# 8. origin ring
mat_ring = bpy.data.materials.new(name="OriginRing_Unlit")
mat_ring.use_nodes = True
bsdf = mat_ring.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.15, 0.1, 0.25, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.15, 0.1, 0.25, 1.0)
bsdf.inputs["Emission Strength"].default_value = 3.0

# --- assign materials ---
assignments = {
    "Floor": mat_floor,
    "Wall_Back": mat_wall,
    "Wall_Front": mat_wall,
    "Wall_Left": mat_wall,
    "Wall_Right": mat_wall,
    "Ceiling": mat_ceiling,
    "Stage_Platform": mat_stage,
    "DJ_Booth": mat_booth,
    "Stage_Backdrop": mat_backdrop,
    "Origin_Focal": mat_origin,
    "Origin_Ring": mat_ring,
}

for obj_name, mat in assignments.items():
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        print(f"{obj_name}: material={mat.name}, slots={len(obj.data.materials)}")
    else:
        print(f"WARNING: {obj_name} not found")

print(f"\ntotal materials created: {len(bpy.data.materials)}")
"""

if __name__ == "__main__":
    import json
    result = execute_code(CODE)
    print(json.dumps(result, indent=2))
