"""phase 3: add spatial flow guides on the floor."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

# === SPATIAL FLOW GUIDES ===
# subtle raised strips on the floor guiding movement from
# entry (front wall, y=+7.5) toward origin (y=0) and stage (y=-5.2)
# also lateral guides connecting origin to the columns

W = 20.0
D = 15.0
H_STRIP = 0.025  # barely raised — feel underfoot in vr, subtle visual
STRIP_W = 0.12   # narrow

created = []

# --- main axis: entry to stage ---
# a center line from front wall to origin
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3.75, H_STRIP/2))
strip = bpy.context.active_object
strip.name = "Flow_CenterEntry"
strip.scale = (STRIP_W, 7.5, H_STRIP)  # from y=0 to y=7.5
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
created.append(strip.name)

# center line from origin to stage front
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.6, H_STRIP/2))
strip = bpy.context.active_object
strip.name = "Flow_CenterStage"
strip.scale = (STRIP_W, 5.2, H_STRIP)  # from y=0 to y=-5.2
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
created.append(strip.name)

# --- lateral guides: radiate from origin at 45-degree angles ---
for i, angle in enumerate([math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]):
    length = 5.0
    cx = math.cos(angle) * length / 2
    cy = math.sin(angle) * length / 2

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, H_STRIP/2))
    strip = bpy.context.active_object
    strip.name = f"Flow_Radial_{i}"
    strip.scale = (length, STRIP_W, H_STRIP)
    strip.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    created.append(strip.name)

# --- join all flow strips into one mesh ---
bpy.ops.object.select_all(action='DESELECT')
for name in created:
    bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[created[0]]
bpy.ops.object.join()
flow = bpy.context.active_object
flow.name = "Floor_FlowGuides"

# apply material — subtle emissive strip
mat_flow = bpy.data.materials.new(name="FlowGuide_Unlit")
mat_flow.use_nodes = True
bsdf = mat_flow.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.08, 0.06, 0.12, 1.0)
bsdf.inputs["Emission Color"].default_value = (0.1, 0.07, 0.16, 1.0)
bsdf.inputs["Emission Strength"].default_value = 2.0
flow.data.materials.clear()
flow.data.materials.append(mat_flow)

polys = len(flow.data.polygons)
print(f"Floor_FlowGuides: {polys} polys, material=FlowGuide_Unlit")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
