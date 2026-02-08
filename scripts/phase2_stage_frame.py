"""phase 2: add angular proscenium arch framing the stage."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy

W = 20.0
D = 15.0
H = 4.0
STAGE_Y_FRONT = -5.2 + 2.0  # front edge of stage area

# === STAGE FRAME / PROSCENIUM ===
# angular gateway form framing the stage
# two vertical pillars + a horizontal lintel
# creates visual hierarchy — marks the stage as focal

FRAME_W = 8.0       # total width of frame opening
PILLAR_W = 0.5
PILLAR_D = 0.4
PILLAR_H = 3.8
LINTEL_H = 0.4
FRAME_Y = STAGE_Y_FRONT  # aligned with front of stage

# left pillar
bpy.ops.mesh.primitive_cube_add(size=1, location=(-FRAME_W/2, FRAME_Y, PILLAR_H/2))
pillar_l = bpy.context.active_object
pillar_l.name = "Frame_Pillar_L"
pillar_l.scale = (PILLAR_W, PILLAR_D, PILLAR_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# right pillar
bpy.ops.mesh.primitive_cube_add(size=1, location=(FRAME_W/2, FRAME_Y, PILLAR_H/2))
pillar_r = bpy.context.active_object
pillar_r.name = "Frame_Pillar_R"
pillar_r.scale = (PILLAR_W, PILLAR_D, PILLAR_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# top lintel
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, FRAME_Y, PILLAR_H + LINTEL_H/2))
lintel = bpy.context.active_object
lintel.name = "Frame_Lintel"
lintel.scale = (FRAME_W + PILLAR_W, PILLAR_D, LINTEL_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# angular accent — chevron/wedge on top of lintel
# adds visual tension, points down toward stage
bpy.ops.mesh.primitive_cone_add(
    vertices=4,
    radius1=1.2,
    radius2=0.0,
    depth=0.6,
    location=(0, FRAME_Y, PILLAR_H + LINTEL_H + 0.05)
)
chevron = bpy.context.active_object
chevron.name = "Frame_Chevron"
chevron.rotation_euler = (3.14159, 0, 0.7854)  # flip and rotate 45deg
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# join all frame pieces into one mesh
bpy.ops.object.select_all(action='DESELECT')
frame_parts = ["Frame_Pillar_L", "Frame_Pillar_R", "Frame_Lintel", "Frame_Chevron"]
for name in frame_parts:
    bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["Frame_Pillar_L"]
bpy.ops.object.join()
frame = bpy.context.active_object
frame.name = "Stage_Frame"

polys = len(frame.data.polygons)
print(f"Stage_Frame: {polys} polys")
"""

result = execute_code(CODE)
print(json.dumps(result, indent=2))
