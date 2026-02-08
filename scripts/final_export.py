"""purge orphans and do final FBX export for Horizon import."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy, os

# --- purge orphan data ---
before_meshes = len(bpy.data.meshes)
before_mats = len(bpy.data.materials)

for block in list(bpy.data.meshes):
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in list(bpy.data.materials):
    if block.users == 0:
        bpy.data.materials.remove(block)
for block in list(bpy.data.images):
    if block.users == 0:
        bpy.data.images.remove(block)
for block in list(bpy.data.textures):
    if block.users == 0:
        bpy.data.textures.remove(block)
for block in list(bpy.data.node_groups):
    if block.users == 0:
        bpy.data.node_groups.remove(block)

after_meshes = len(bpy.data.meshes)
after_mats = len(bpy.data.materials)
print('purged: %d orphan meshes, %d orphan materials' % (before_meshes - after_meshes, before_mats - after_mats))

# --- verify all transforms applied ---
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(False)
print('transforms applied')

# --- export FBX ---
export_dir = '/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx'
os.makedirs(export_dir, exist_ok=True)
path = os.path.join(export_dir, 'pg_origin_club_final.fbx')

bpy.ops.export_scene.fbx(
    filepath=path,
    use_selection=False,
    apply_scale_options='FBX_SCALE_ALL',
    apply_unit_scale=True,
    bake_space_transform=True,
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
    add_leaf_bones=False,
    path_mode='COPY',
    embed_textures=True,
    object_types={'MESH', 'LIGHT', 'CAMERA'},
)
size = os.path.getsize(path)
print('exported: %s (%.1f kb)' % (path, size/1024))

# --- save blend ---
bpy.ops.wm.save_as_mainfile(
    filepath='/Users/chanceneihouse/GitHub/world-builder-agent/world/pg_origin_club.blend'
)
print('blend saved')

# --- final count ---
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
tp = sum(len(o.data.polygons) for o in meshes)
tt = sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes)
lights = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
mats = len(bpy.data.materials)
print()
print('FINAL: %d meshes, %d polys, %d tris, %d materials, %d lights' % (len(meshes), tp, tt, mats, lights))
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
