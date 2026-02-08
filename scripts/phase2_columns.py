"""phase 2: add rhythmic wall columns along left and right walls."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

W = 20.0
D = 15.0
H = 4.0

# === RHYTHMIC WALL COLUMNS ===
# evenly spaced along left and right walls
# tapered hexagonal columns — 6 per side, 12 total
# spacing creates visual rhythm like a beat grid

NUM_COLUMNS = 6
SPACING = D / (NUM_COLUMNS + 1)  # even spacing along y-axis
COL_RADIUS_BASE = 0.25
COL_RADIUS_TOP = 0.18
COL_HEIGHT = 3.6  # slightly shorter than room height
COL_SEGMENTS = 6  # hexagonal

# offset from wall
WALL_OFFSET = 0.4

created = []

for side_name, x_pos in [("L", -W/2 + WALL_OFFSET), ("R", W/2 - WALL_OFFSET)]:
    for i in range(NUM_COLUMNS):
        y_pos = -D/2 + SPACING * (i + 1)
        col_name = f"Column_{side_name}_{i+1:02d}"

        # create tapered cylinder
        bpy.ops.mesh.primitive_cone_add(
            vertices=COL_SEGMENTS,
            radius1=COL_RADIUS_BASE,
            radius2=COL_RADIUS_TOP,
            depth=COL_HEIGHT,
            location=(x_pos, y_pos, COL_HEIGHT / 2)
        )
        col = bpy.context.active_object
        col.name = col_name
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        created.append(col_name)

# join all left columns into one mesh
bpy.ops.object.select_all(action='DESELECT')
left_cols = [bpy.data.objects[n] for n in created if n.startswith("Column_L")]
for obj in left_cols:
    obj.select_set(True)
bpy.context.view_layer.objects.active = left_cols[0]
bpy.ops.object.join()
joined_left = bpy.context.active_object
joined_left.name = "Columns_Left"

# join all right columns into one mesh
bpy.ops.object.select_all(action='DESELECT')
right_cols = [bpy.data.objects[n] for n in created if n.startswith("Column_R")]
for obj in right_cols:
    obj.select_set(True)
bpy.context.view_layer.objects.active = right_cols[0]
bpy.ops.object.join()
joined_right = bpy.context.active_object
joined_right.name = "Columns_Right"

for name in ["Columns_Left", "Columns_Right"]:
    obj = bpy.data.objects[name]
    polys = len(obj.data.polygons)
    print(f"{name}: {polys} polys")
"""

result = execute_code(CODE)
print(json.dumps(result, indent=2))
