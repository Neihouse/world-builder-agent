"""check and fix backdrop relief positioning relative to screen and back wall."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

print('=== BACKDROP RELIEF POSITION CHECK ===')
print()

relief = bpy.data.objects.get('Backdrop_Relief')
screen = bpy.data.objects.get('Stage_Screen')
wall = bpy.data.objects.get('Wall_Back')

for name, obj in [('Relief', relief), ('Screen', screen), ('Wall_Back', wall)]:
    if obj:
        verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
        xs = [v.x for v in verts]
        ys = [v.y for v in verts]
        zs = [v.z for v in verts]
        print('%s:' % name)
        print('  x: [%.2f to %.2f] (width: %.2f)' % (min(xs), max(xs), max(xs)-min(xs)))
        print('  y: [%.2f to %.2f] (depth: %.2f)' % (min(ys), max(ys), max(ys)-min(ys)))
        print('  z: [%.2f to %.2f] (height: %.2f)' % (min(zs), max(zs), max(zs)-min(zs)))
        print()

# the relief should sit ON the front face of the screen, not clip through the wall
# screen front face: y = -9.4 (screen spans -9.6 to -9.4)
# relief should be at y ~ -9.3 to -9.35 (just in front of screen)
# back wall back face: y = -10.1

if relief:
    rv = [relief.matrix_world @ v.co for v in relief.data.vertices]
    relief_ymin = min(v.y for v in rv)
    relief_ymax = max(v.y for v in rv)
    relief_center_y = (relief_ymin + relief_ymax) / 2

    print('PROBLEM: relief extends to y=%.2f (behind back wall at y=-10.1)' % relief_ymin)
    print('Relief center y = %.2f' % relief_center_y)
    print()

    # place relief so its BACK face sits at screen front face (y=-9.45)
    # relief depth = relief_ymax - relief_ymin
    relief_depth = relief_ymax - relief_ymin
    target_back = -9.45  # screen front face
    target_center_y = target_back + relief_depth / 2
    shift = target_center_y - relief_center_y
    print('Shifting relief by %.2f in Y to center at y=%.2f' % (shift, target_center_y))

    # move all vertices
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(relief.data)
    for v in bm.verts:
        v.co.y += shift
    bm.to_mesh(relief.data)
    bm.free()
    relief.data.update()

    # verify
    rv2 = [relief.matrix_world @ v.co for v in relief.data.vertices]
    print()
    print('AFTER FIX:')
    print('  Relief y: [%.2f to %.2f]' % (min(v.y for v in rv2), max(v.y for v in rv2)))
    print('  Screen y: [%.2f to %.2f]' % (
        min(v.y for v in [screen.matrix_world @ v.co for v in screen.data.vertices]),
        max(v.y for v in [screen.matrix_world @ v.co for v in screen.data.vertices])))
    print('  Wall   y: [%.2f to %.2f]' % (
        min(v.y for v in [wall.matrix_world @ v.co for v in wall.data.vertices]),
        max(v.y for v in [wall.matrix_world @ v.co for v in wall.data.vertices])))

    # check no clipping
    new_ymin = min(v.y for v in rv2)
    wall_ymax = max(v.y for v in [wall.matrix_world @ v.co for v in wall.data.vertices])
    screen_ymax = max(v.y for v in [screen.matrix_world @ v.co for v in screen.data.vertices])
    print()
    if new_ymin > wall_ymax:
        print('OK: relief is in front of back wall (gap: %.2fm)' % (new_ymin - wall_ymax))
    else:
        print('PROBLEM: relief still clips through back wall')
    if new_ymin > screen_ymax - 0.1:
        print('OK: relief sits on screen surface')
    else:
        print('WARNING: relief may be behind screen surface')
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
