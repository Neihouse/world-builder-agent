"""fix walls — they're still v1 dimensions (4m tall, 15m room) but room is v2 (7m, 20m)."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

W = 20.0
H = 7.0
WALL_T = 0.3
MAIN_BACK = -10.0
MAIN_FRONT = 5.0
ENTRY_FRONT = 10.0
D_TOTAL = ENTRY_FRONT - MAIN_BACK  # 20m

print('=== FIXING WALLS ===')
print()

# --- delete old walls (back, left, right) ---
for name in ['Wall_Back', 'Wall_Left', 'Wall_Right']:
    obj = bpy.data.objects.get(name)
    if obj:
        # report old dimensions
        verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
        ys = [v.y for v in verts]
        zs = [v.z for v in verts]
        print('OLD %s: y=[%.1f to %.1f] z=[%.1f to %.1f]' % (name, min(ys), max(ys), min(zs), max(zs)))
        bpy.data.objects.remove(obj, do_unlink=True)

# --- rebuild back wall at y=-10, full 7m height ---
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, MAIN_BACK, H/2))
o = bpy.context.active_object
o.name = 'Wall_Back'
o.scale = (W + WALL_T*2, WALL_T, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# assign material
mat = bpy.data.materials.get('DarkWall_Metal')
if mat:
    o.data.materials.clear()
    o.data.materials.append(mat)

# --- rebuild left wall — full depth, full height ---
bpy.ops.mesh.primitive_cube_add(size=1, location=(-W/2, (MAIN_BACK + MAIN_FRONT)/2, H/2))
o = bpy.context.active_object
o.name = 'Wall_Left'
o.scale = (WALL_T, MAIN_FRONT - MAIN_BACK, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

mat = bpy.data.materials.get('DarkWall_Metal')
if mat:
    o.data.materials.clear()
    o.data.materials.append(mat)

# --- rebuild right wall — full depth, full height ---
bpy.ops.mesh.primitive_cube_add(size=1, location=(W/2, (MAIN_BACK + MAIN_FRONT)/2, H/2))
o = bpy.context.active_object
o.name = 'Wall_Right'
o.scale = (WALL_T, MAIN_FRONT - MAIN_BACK, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

mat = bpy.data.materials.get('DarkWall_Metal')
if mat:
    o.data.materials.clear()
    o.data.materials.append(mat)

# --- apply transforms to new walls ---
for name in ['Wall_Back', 'Wall_Left', 'Wall_Right']:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(False)

# --- verify ---
print()
print('NEW WALLS:')
for name in ['Wall_Back', 'Wall_Left', 'Wall_Right', 'Wall_Front_L', 'Wall_Front_R', 'Wall_Entry_L', 'Wall_Entry_R']:
    obj = bpy.data.objects.get(name)
    if obj:
        verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
        ys = [v.y for v in verts]
        zs = [v.z for v in verts]
        xs = [v.x for v in verts]
        print('  %s: x=[%.1f,%.1f] y=[%.1f,%.1f] z=[%.1f,%.1f]' % (
            name, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

# check screen vs back wall
screen = bpy.data.objects.get('Stage_Screen')
wall = bpy.data.objects.get('Wall_Back')
if screen and wall:
    sv = [screen.matrix_world @ v.co for v in screen.data.vertices]
    wv = [wall.matrix_world @ v.co for v in wall.data.vertices]
    print()
    print('Screen y=[%.1f,%.1f], Back wall y=[%.1f,%.1f]' % (
        min(v.y for v in sv), max(v.y for v in sv),
        min(v.y for v in wv), max(v.y for v in wv)))
    print('Screen is %.1fm in front of back wall' % (min(v.y for v in sv) - max(v.y for v in wv)))
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
