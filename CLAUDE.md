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
| max texture resolution | 4096x4096 (recommended: 1024 for Quest perf) |
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

## critical import notes (from research)

**these are things Blender CANNOT do for Horizon — must be done in the Horizon Desktop Editor:**

- **materials**: Blender material properties (roughness, metallic, emission values) are IGNORED on import. only the material name suffix matters. to transfer appearance, must bake textures into channel-packed PNGs (_BR for base+roughness, _MEO for metal+emissive+AO).
- **lighting**: all Blender lights are IGNORED on import. must recreate using Static Light and Dynamic Light Gizmos in Horizon.
- **emissive glow**: _Unlit materials appear bright but do NOT cast light on surroundings. pair with light gizmos.
- **no bloom**: Quest has no post-processing. glow effects must be faked with particles + lights.
- **scripting**: Horizon uses TypeScript for interactivity. audio triggers, light animation, UI panels all done via TS in the Desktop Editor.
- **audio**: no live streaming. pre-recorded files only (up to 20 min loops). spatial audio via Sound Recorder Gizmo.
- **desktop editor**: Windows only. no macOS support.

### texture channel packing (for baked textures)

| texture | suffix | R | G | B | A |
|---|---|---|---|---|---|
| TextureA | `_BR` | base R | base G | base B | roughness |
| TextureB | `_MEO` | metalness | emissive | AO | (opacity) |

### horizon gizmos relevant to our venue

| gizmo | purpose |
|---|---|
| Static Light | baked point/spot/directional lights |
| Dynamic Light | scriptable lights for light shows |
| Environment | ambient light, fog, skybox |
| Sound Recorder | spatial audio sources, 20 min max |
| Spawn Point | player entry position + facing |
| Trigger Zone | detect players in areas (dance floor, VIP) |
| Custom UI | interactive panels (DJ booth controls) |
| ParticleFX | fog, sparks, haze effects |
| Script | TypeScript logic |

## tone

- lowercase only
- factual
- no filler
- execution-focused
