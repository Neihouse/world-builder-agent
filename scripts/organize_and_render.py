"""organize into collections and render viewer perspective shots."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

# Step 1: Organize into collections
CODE1 = r"""
import bpy

# remove all existing collections except Scene Collection
for col in list(bpy.data.collections):
    bpy.data.collections.remove(col)

# define collections and their objects
collections = {
    'Shell': ['Floor', 'Wall_Back', 'Wall_Left', 'Wall_Right', 'Wall_Front_L', 'Wall_Front_R',
              'Wall_Entry_L', 'Wall_Entry_R', 'Ceiling_Main', 'Ceiling_Entry'],
    'Stage': ['Stage_Platform', 'Stage_Edge', 'DJ_Booth', 'Stage_Screen'],
    'DanceFloor': ['DanceFloor_Tier1', 'Origin_Focal', 'Origin_Ring', 'Spawn_Marker'],
    'Identity': ['Columns_L', 'Columns_R', 'Stage_Frame', 'Totem_L', 'Totem_R',
                 'Backdrop_Relief', 'Ceiling_Beams', 'Floor_FlowGuides'],
    'Lighting': [],  # lights go here
}

scene_col = bpy.context.scene.collection

for col_name, obj_names in collections.items():
    col = bpy.data.collections.new(col_name)
    scene_col.children.link(col)

    for obj_name in obj_names:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            # unlink from scene collection
            for c in obj.users_collection:
                c.objects.unlink(obj)
            col.objects.link(obj)

# move lights and camera to Lighting collection
light_col = bpy.data.collections.get('Lighting')
for obj in bpy.data.objects:
    if obj.type in ('LIGHT', 'CAMERA'):
        for c in obj.users_collection:
            c.objects.unlink(obj)
        light_col.objects.link(obj)

# report
for col in bpy.data.collections:
    names = [o.name for o in col.objects]
    print('%s (%d): %s' % (col.name, len(names), ', '.join(names)))
"""

print("--- organizing collections ---")
r = execute_code(CODE1)
print(r.get("result", {}).get("result", r))

# Step 2: Render viewer perspective shots
CODE2 = r"""
import bpy, os, math

cam = bpy.data.objects.get('Camera_Main')
if not cam:
    bpy.ops.object.camera_add(location=(0, 8.0, 1.7))
    cam = bpy.context.active_object
    cam.name = 'Camera_Main'

scene = bpy.context.scene
scene.camera = cam
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.eevee.taa_render_samples = 64

render_dir = '/Users/chanceneihouse/GitHub/world-builder-agent/world/renders'
os.makedirs(render_dir, exist_ok=True)

# shot 1: spawn point view — what the player sees first
# standing at spawn (y=3), eye height 1.7m, looking toward stage (negative y)
cam.location = (0, 3.0, 1.7)
cam.rotation_euler = (math.radians(90), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, 'view_spawn.png')
bpy.ops.render.render(write_still=True)
print('rendered: spawn point view (what player sees on entry)')

# shot 2: dance floor — at origin, looking at stage
cam.location = (0, 0.0, 1.7)
cam.rotation_euler = (math.radians(88), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, 'view_dancefloor.png')
bpy.ops.render.render(write_still=True)
print('rendered: dance floor view (at origin focal)')

# shot 3: front row — tier 1, closest to stage
cam.location = (0, -3.0, 1.9)
cam.rotation_euler = (math.radians(85), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, 'view_frontrow.png')
bpy.ops.render.render(write_still=True)
print('rendered: front row view (tier 1)')

# shot 4: looking back from stage — DJ perspective toward audience
cam.location = (0, -6.5, 2.8)
cam.rotation_euler = (math.radians(88), 0, 0)
cam.data.lens = 18
scene.render.filepath = os.path.join(render_dir, 'view_dj_perspective.png')
bpy.ops.render.render(write_still=True)
print('rendered: DJ perspective (looking at audience)')

# shot 5: entry corridor — looking in from entrance
cam.location = (0, 9.5, 1.7)
cam.rotation_euler = (math.radians(90), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, 'view_entrance.png')
bpy.ops.render.render(write_still=True)
print('rendered: entrance corridor view')

# shot 6: wide corner — overview of the whole space
cam.location = (8, 3, 4.0)
cam.rotation_euler = (math.radians(75), 0, math.radians(150))
cam.data.lens = 18
scene.render.filepath = os.path.join(render_dir, 'view_wide.png')
bpy.ops.render.render(write_still=True)
print('rendered: wide corner overview')

# reset camera
cam.data.lens = 50
"""

print("\n--- rendering viewer perspectives ---")
r = execute_code(CODE2)
print(r.get("result", {}).get("result", r))
