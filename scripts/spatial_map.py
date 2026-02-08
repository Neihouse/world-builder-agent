"""map the full spatial layout of every object — world-space bounds."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

print('=== SPATIAL MAP (world-space vertex bounds) ===')
print()

meshes = sorted([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: o.name)

for obj in meshes:
    verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    xs = [v.x for v in verts]
    ys = [v.y for v in verts]
    zs = [v.z for v in verts]
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    cz = (min(zs) + max(zs)) / 2
    w = max(xs) - min(xs)
    d = max(ys) - min(ys)
    h = max(zs) - min(zs)
    print('%-20s center=(%.1f, %.1f, %.1f)  size=(%.1f x %.1f x %.1f)  y=[%.1f to %.1f]  z=[%.1f to %.1f]' % (
        obj.name, cx, cy, cz, w, d, h, min(ys), max(ys), min(zs), max(zs)))

print()
print('=== LAYOUT VERIFICATION ===')
print()

# verify spatial ordering (audience perspective: y=+10 entrance, y=-10 back wall)
stage_plat = bpy.data.objects.get('Stage_Platform')
dj = bpy.data.objects.get('DJ_Booth')
screen = bpy.data.objects.get('Stage_Screen')
frame = bpy.data.objects.get('Stage_Frame')
relief = bpy.data.objects.get('Backdrop_Relief')
tier1 = bpy.data.objects.get('DanceFloor_Tier1')
origin = bpy.data.objects.get('Origin_Focal')
spawn = bpy.data.objects.get('Spawn_Marker')

def get_y_range(obj):
    if not obj:
        return None, None
    verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    ys = [v.y for v in verts]
    return min(ys), max(ys)

print('EXPECTED ORDER (audience y=+10 walks toward stage y=-10):')
print('  entrance (y=+10) -> corridor -> spawn (y~3) -> origin (y=0) -> tier1 -> stage -> DJ -> screen -> back wall (y=-10)')
print()

elements = [
    ('Spawn_Marker', spawn),
    ('Origin_Focal', origin),
    ('DanceFloor_Tier1', tier1),
    ('Stage_Platform', stage_plat),
    ('DJ_Booth', dj),
    ('Stage_Screen', screen),
    ('Stage_Frame', frame),
    ('Backdrop_Relief', relief),
]

print('ACTUAL Y POSITIONS:')
for name, obj in elements:
    ymin, ymax = get_y_range(obj)
    if ymin is not None:
        print('  %-20s y = %.1f to %.1f  (center: %.1f)' % (name, ymin, ymax, (ymin+ymax)/2))
    else:
        print('  %-20s MISSING' % name)

print()
print('CHECKS:')

# DJ should be between stage front and screen
if dj and screen and stage_plat:
    dj_ymin, dj_ymax = get_y_range(dj)
    screen_ymin, screen_ymax = get_y_range(screen)
    stage_ymin, stage_ymax = get_y_range(stage_plat)

    if dj_ymin > screen_ymax:
        print('  OK: DJ booth is in front of screen')
    else:
        print('  PROBLEM: DJ booth overlaps or is behind screen')

    if dj_ymax < stage_ymax:
        print('  OK: DJ booth is within stage depth')
    else:
        print('  WARNING: DJ booth extends past stage front')

# screen should be against back wall
if screen:
    screen_ymin, screen_ymax = get_y_range(screen)
    back_wall = bpy.data.objects.get('Wall_Back')
    if back_wall:
        wall_ymin, wall_ymax = get_y_range(back_wall)
        gap = screen_ymin - wall_ymax
        print('  Screen-to-back-wall gap: %.1fm %s' % (abs(gap), '(OK)' if abs(gap) < 1.0 else '(TOO FAR)'))

# stage should be elevated
if stage_plat:
    verts = [stage_plat.matrix_world @ v.co for v in stage_plat.data.vertices]
    stage_top = max(v.z for v in verts)
    print('  Stage top surface: z=%.1fm %s' % (stage_top, '(OK - good VR sightline)' if stage_top >= 1.0 else '(TOO LOW)'))

# DJ booth should be above stage
if dj and stage_plat:
    dj_verts = [dj.matrix_world @ v.co for v in dj.data.vertices]
    dj_bottom = min(v.z for v in dj_verts)
    dj_top = max(v.z for v in dj_verts)
    print('  DJ booth: z=%.1f to z=%.1f (should be above stage at z=%.1f)' % (dj_bottom, dj_top, stage_top))

# screen should be above stage, visible to audience
if screen and stage_plat:
    screen_verts = [screen.matrix_world @ v.co for v in screen.data.vertices]
    screen_bottom = min(v.z for v in screen_verts)
    screen_top = max(v.z for v in screen_verts)
    print('  Screen: z=%.1f to z=%.1f (visible from dance floor? %s)' % (
        screen_bottom, screen_top, 'YES' if screen_bottom >= stage_top else 'PARTIALLY BLOCKED'))

# spawn marker should face stage (negative y direction)
if spawn:
    spawn_verts = [spawn.matrix_world @ v.co for v in spawn.data.vertices]
    spawn_y = sum(v.y for v in spawn_verts) / len(spawn_verts)
    print('  Spawn point: y=%.1f (distance to stage front: %.1fm)' % (spawn_y, abs(spawn_y - stage_ymax)))

# columns should be along walls
cols_l = bpy.data.objects.get('Columns_L')
cols_r = bpy.data.objects.get('Columns_R')
if cols_l and cols_r:
    l_verts = [cols_l.matrix_world @ v.co for v in cols_l.data.vertices]
    r_verts = [cols_r.matrix_world @ v.co for v in cols_r.data.vertices]
    l_x = sum(v.x for v in l_verts) / len(l_verts)
    r_x = sum(v.x for v in r_verts) / len(r_verts)
    print('  Columns L avg x=%.1f, Columns R avg x=%.1f (walls at x=+-10)' % (l_x, r_x))

# entry corridor
entry_l = bpy.data.objects.get('Wall_Entry_L')
entry_r = bpy.data.objects.get('Wall_Entry_R')
if entry_l and entry_r:
    el_verts = [entry_l.matrix_world @ v.co for v in entry_l.data.vertices]
    er_verts = [entry_r.matrix_world @ v.co for v in entry_r.data.vertices]
    el_x = sum(v.x for v in el_verts) / len(el_verts)
    er_x = sum(v.x for v in er_verts) / len(er_verts)
    el_yrange = (min(v.y for v in el_verts), max(v.y for v in el_verts))
    print('  Entry corridor walls: x=%.1f and x=%.1f, y=%.1f to %.1f' % (el_x, er_x, el_yrange[0], el_yrange[1]))

# totems flanking screen
totem_l = bpy.data.objects.get('Totem_L')
totem_r = bpy.data.objects.get('Totem_R')
if totem_l and totem_r:
    tl_verts = [totem_l.matrix_world @ v.co for v in totem_l.data.vertices]
    tr_verts = [totem_r.matrix_world @ v.co for v in totem_r.data.vertices]
    tl_x = sum(v.x for v in tl_verts) / len(tl_verts)
    tr_x = sum(v.x for v in tr_verts) / len(tr_verts)
    tl_y = sum(v.y for v in tl_verts) / len(tl_verts)
    print('  Totems: L x=%.1f, R x=%.1f, y~%.1f (should flank screen)' % (tl_x, tr_x, tl_y))
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
