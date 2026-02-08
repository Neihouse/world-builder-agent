# world-builder-agent

## agent behavior

this project follows `agents.md` as the primary directive. read it before any build action.

the agent operates blender via mcp to build a vr club world for meta horizon worlds. the founder does not perform 3d work. the agent executes autonomously.

## platform constraints (meta horizon worlds)

these are hard limits. violating any of these is a build failure.

| constraint | limit |
|---|---|
| format | fbx |
| max polys per object | 50,000 |
| max textures per material | 2 |
| max texture resolution | 2048x2048 |
| texture format | png |
| max materials per object | 2 |
| custom shaders | not allowed |
| animations | not allowed unless explicitly requested |
| world storage limit | 6 gb |
| target framerate | 72 fps |
| target draw calls | < 100 per view |

### material naming convention (horizon worlds)

materials must use suffix tags for horizon compatibility:

- `_Metal` — single texture metal pbr
- `_Unlit` — unlit material (use for emissive-style panels)
- `_Blend` — unlit blend
- `_Transparent` — transparent material
- `_Masked` — masked material
- `_VXC` — vertex color pbr
- `_VXM` — vertex single texture

avoid special characters in names: `- . , / * $ &`
avoid underscores in names except for recognized suffix tags above.

### fbx export settings (blender)

always use these settings when exporting:

```python
bpy.ops.export_scene.fbx(
    filepath='<target_path>',
    use_selection=False,
    apply_scale_options='FBX_SCALE_ALL',
    apply_unit_scale=True,
    bake_space_transform=True,
    mesh_smooth_type='FACE',
    use_mesh_modifiers=True,
    add_leaf_bones=False,
    path_mode='COPY',
    embed_textures=True
)
```

### scale

- blender default: meters
- fbx default: centimeters
- use `FBX_SCALE_ALL` + `apply_unit_scale=True` to handle conversion
- vr human scale: ~1.7m standing height. use this as reference.

## decision rules

- performance > aesthetics. always.
- simple geometry > realism
- repetition > uniqueness
- lighting > texture detail
- fewer meshes > many objects
- if in doubt, decimate harder

## project structure

```
/world/fbx/          — final exports
/world/assets/       — downloaded source assets
/world/docs/         — asset-log.md, build-notes.md
/agents.md           — agent directive
/CLAUDE.md           — this file
/.mcp.json           — blender mcp config
```

## blender mcp usage

the agent connects to blender via the `blender-mcp` server. blender must be running with the blendermcp addon active on port 9876.

key tools:
- `execute_blender_code` — run arbitrary bpy python in blender
- `get_scene_info` — inspect current scene state
- `get_object_info` — inspect specific object
- `get_viewport_screenshot` — visual verification
- `search_polyhaven_assets` / `download_polyhaven_asset` — poly haven integration
- `search_sketchfab_models` / `download_sketchfab_model` — sketchfab integration

## tone

- lowercase only
- factual
- no filler
- execution-focused
