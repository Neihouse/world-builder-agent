"""phase 3: add ceiling beams for depth and underground bunker feel."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

W = 20.0
D = 15.0
H = 4.0

# === CEILING BEAMS ===
# 5 cross-beams running left-right (along x axis)
# evenly spaced along y, at ceiling height
# creates underground bunker / industrial feel
# merged into single mesh to minimize draw calls

NUM_BEAMS = 5
BEAM_H = 0.25
BEAM_D = 0.3  # depth along y
BEAM_W = W    # span full width
SPACING = D / (NUM_BEAMS + 1)

beam_names = []

for i in range(NUM_BEAMS):
    y_pos = -D/2 + SPACING * (i + 1)

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, y_pos, H - BEAM_H/2)
    )
    beam = bpy.context.active_object
    beam.name = f"Beam_{i}"
    beam.scale = (BEAM_W, BEAM_D, BEAM_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    beam_names.append(beam.name)

# join all beams
bpy.ops.object.select_all(action='DESELECT')
for name in beam_names:
    bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[beam_names[0]]
bpy.ops.object.join()
beams = bpy.context.active_object
beams.name = "Ceiling_Beams"

# material — same as ceiling but slightly lighter to catch light
mat_beam = bpy.data.materials.new(name="BeamConcrete_Metal")
mat_beam.use_nodes = True
bsdf = mat_beam.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.035, 0.035, 0.04, 1.0)
bsdf.inputs["Roughness"].default_value = 0.85
bsdf.inputs["Metallic"].default_value = 0.1
beams.data.materials.clear()
beams.data.materials.append(mat_beam)

polys = len(beams.data.polygons)
print(f"Ceiling_Beams: {polys} polys, material=BeamConcrete_Metal")
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
