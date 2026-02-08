"""render the rebuilt club from multiple angles."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy, os, math

cam = bpy.data.objects["Camera_Main"]
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.eevee.taa_render_samples = 64

render_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world/renders"
os.makedirs(render_dir, exist_ok=True)

# save + re-export first
bpy.ops.export_scene.fbx(
    filepath="/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx/pg_origin_club_final.fbx",
    use_selection=False,
    apply_scale_options='FBX_SCALE_ALL', apply_unit_scale=True,
    bake_space_transform=True, mesh_smooth_type='FACE',
    use_mesh_modifiers=True, add_leaf_bones=False,
    path_mode='COPY', embed_textures=True,
    object_types={'MESH', 'LIGHT', 'CAMERA'},
)
bpy.ops.wm.save_as_mainfile(filepath="/Users/chanceneihouse/GitHub/world-builder-agent/world/pg_origin_club.blend")

# shot 1: entry corridor looking toward stage (first person spawn view)
cam.location = (0, 7.0, 1.7)
cam.rotation_euler = (math.radians(87), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, "rebuild_spawn_view.png")
bpy.ops.render.render(write_still=True)
print("rendered: spawn view")

# shot 2: dance floor looking at stage
cam.location = (0, 1.0, 1.7)
cam.rotation_euler = (math.radians(85), 0, math.radians(180))
cam.data.lens = 24
scene.render.filepath = os.path.join(render_dir, "rebuild_dancefloor.png")
bpy.ops.render.render(write_still=True)
print("rendered: dance floor view")

# shot 3: wide corner
cam.location = (8, 3, 3.0)
cam.rotation_euler = (math.radians(78), 0, math.radians(155))
cam.data.lens = 18
scene.render.filepath = os.path.join(render_dir, "rebuild_wide.png")
bpy.ops.render.render(write_still=True)
print("rendered: wide view")

cam.data.lens = 50
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
