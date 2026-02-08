"""full rebuild — research-informed stage and room layout."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

# ============================================================
# STEP 1: CLEAR SCENE
# ============================================================
print("--- clearing scene ---")
r = execute_code("""
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
# purge orphan data
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
print(f"scene cleared: {len(bpy.data.objects)} objects")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 2: BUILD SHELL — taller ceiling, entry corridor
# ============================================================
print("\n--- building shell ---")
r = execute_code(r"""
import bpy

# === DIMENSIONS ===
W = 20.0        # room width
D_MAIN = 15.0   # main room depth
D_ENTRY = 5.0   # entry corridor depth
D_TOTAL = D_MAIN + D_ENTRY  # 20m total
H = 7.0         # ceiling height (was 4m, now 7m)
WALL_T = 0.3
ENTRY_W = 6.0   # corridor width (narrower than main room)
ENTRY_H = 3.5   # corridor ceiling (lower, creates reveal moment)

# main room spans y = -10 (back wall) to y = +5 (where corridor begins)
# corridor spans y = +5 to y = +10 (front entrance)
MAIN_BACK = -10.0
MAIN_FRONT = 5.0
ENTRY_FRONT = 10.0

# --- FLOOR (full length) ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor.scale = (W, D_TOTAL, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# --- MAIN ROOM WALLS ---
# back wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, MAIN_BACK, H/2))
o = bpy.context.active_object
o.name = "Wall_Back"
o.scale = (W + WALL_T*2, WALL_T, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# left wall (full length)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-W/2, 0, H/2))
o = bpy.context.active_object
o.name = "Wall_Left"
o.scale = (WALL_T, D_TOTAL, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# right wall (full length)
bpy.ops.mesh.primitive_cube_add(size=1, location=(W/2, 0, H/2))
o = bpy.context.active_object
o.name = "Wall_Right"
o.scale = (WALL_T, D_TOTAL, H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# front wall (with entry opening) — two sections flanking the corridor
for side, x_offset in [("L", -(ENTRY_W/2 + (W/2 - ENTRY_W/2)/2)), ("R", (ENTRY_W/2 + (W/2 - ENTRY_W/2)/2))]:
    section_w = W/2 - ENTRY_W/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_offset, ENTRY_FRONT, H/2))
    o = bpy.context.active_object
    o.name = f"Wall_Front_{side}"
    o.scale = (section_w, WALL_T, H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# --- ENTRY CORRIDOR WALLS ---
# left corridor wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ENTRY_W/2, (MAIN_FRONT + ENTRY_FRONT)/2, ENTRY_H/2))
o = bpy.context.active_object
o.name = "Wall_Entry_L"
o.scale = (WALL_T, D_ENTRY, ENTRY_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# right corridor wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(ENTRY_W/2, (MAIN_FRONT + ENTRY_FRONT)/2, ENTRY_H/2))
o = bpy.context.active_object
o.name = "Wall_Entry_R"
o.scale = (WALL_T, D_ENTRY, ENTRY_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# --- CEILINGS ---
# main room ceiling
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (MAIN_BACK + MAIN_FRONT)/2, H))
o = bpy.context.active_object
o.name = "Ceiling_Main"
o.scale = (W, D_MAIN, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# entry corridor ceiling (lower)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (MAIN_FRONT + ENTRY_FRONT)/2, ENTRY_H))
o = bpy.context.active_object
o.name = "Ceiling_Entry"
o.scale = (ENTRY_W, D_ENTRY, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

meshes = [o for o in bpy.data.objects if o.type == "MESH"]
total_p = sum(len(o.data.polygons) for o in meshes)
print(f"shell built: {len(meshes)} meshes, {total_p} polys")
for m in sorted(meshes, key=lambda o: o.name):
    print(f"  {m.name}: {len(m.data.polygons)}p")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 3: STAGE — 1.5m elevated, against back wall
# ============================================================
print("\n--- building stage ---")
r = execute_code(r"""
import bpy

MAIN_BACK = -10.0
STAGE_W = 10.0
STAGE_D = 5.0
STAGE_H = 1.5
STAGE_Y = MAIN_BACK + STAGE_D/2 + 0.3  # offset from back wall

# stage platform
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, STAGE_Y, STAGE_H/2))
o = bpy.context.active_object
o.name = "Stage_Platform"
o.scale = (STAGE_W, STAGE_D, STAGE_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# stage front face — angled lip for visual definition
# (just a thin strip at front edge of stage)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, STAGE_Y + STAGE_D/2, STAGE_H/2))
o = bpy.context.active_object
o.name = "Stage_Edge"
o.scale = (STAGE_W + 0.4, 0.15, STAGE_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# DJ booth desk on stage
BOOTH_W = 4.5
BOOTH_D = 1.0
BOOTH_H = 1.1
BOOTH_Y = STAGE_Y - 0.5  # toward front of stage

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, BOOTH_Y, STAGE_H + BOOTH_H/2))
o = bpy.context.active_object
o.name = "DJ_Booth"
o.scale = (BOOTH_W, BOOTH_D, BOOTH_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# backdrop / video screen — large, behind DJ, against back wall
SCREEN_W = 9.0
SCREEN_H = 4.5
SCREEN_Y = MAIN_BACK + 0.5  # near back wall

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, SCREEN_Y, STAGE_H + SCREEN_H/2))
o = bpy.context.active_object
o.name = "Stage_Screen"
o.scale = (SCREEN_W, 0.1, SCREEN_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

for name in ["Stage_Platform", "Stage_Edge", "DJ_Booth", "Stage_Screen"]:
    obj = bpy.data.objects[name]
    print(f"{name}: {len(obj.data.polygons)}p")

print(f"\nstage top at z={STAGE_H}m, screen top at z={STAGE_H + SCREEN_H}m")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 4: DANCE FLOOR — tiered, semicircular near stage
# ============================================================
print("\n--- building dance floor ---")
r = execute_code(r"""
import bpy
import math

# tiered dance floor in front of stage
# tier 1: closest to stage, slightly raised (0.2m) — front row
# tier 2: middle zone, ground level — main dance area
# origin focal stays at center

STAGE_FRONT_Y = -7.2 + 2.5  # front edge of stage = STAGE_Y + STAGE_D/2 = -7.2 + 2.5 = -4.7

# tier 1 — raised platform close to stage (front row area)
TIER1_W = 12.0
TIER1_D = 3.0
TIER1_H = 0.2
TIER1_Y = STAGE_FRONT_Y + TIER1_D/2 + 0.5  # gap from stage edge

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, TIER1_Y, TIER1_H/2))
o = bpy.context.active_object
o.name = "DanceFloor_Tier1"
o.scale = (TIER1_W, TIER1_D, TIER1_H)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# origin focal — octagonal disc at center of main floor
ORIGIN_Y = 0.0
ORIGIN_R = 3.5

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=ORIGIN_R, depth=0.05, location=(0, ORIGIN_Y, 0.025))
o = bpy.context.active_object
o.name = "Origin_Focal"
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# origin ring
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=ORIGIN_R + 0.3, depth=0.08, location=(0, ORIGIN_Y, 0.04))
o = bpy.context.active_object
o.name = "Origin_Ring"
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# spawn point marker — 7m from stage, facing it
SPAWN_Y = 3.0
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.0, depth=0.03, location=(0, SPAWN_Y, 0.015))
o = bpy.context.active_object
o.name = "Spawn_Marker"
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

for name in ["DanceFloor_Tier1", "Origin_Focal", "Origin_Ring", "Spawn_Marker"]:
    obj = bpy.data.objects[name]
    print(f"{name}: {len(obj.data.polygons)}p")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 5: IDENTITY — columns, frame, totems, relief, ceiling beams
# ============================================================
print("\n--- building identity elements ---")
r = execute_code(r"""
import bpy
import math

W = 20.0
H = 7.0
MAIN_BACK = -10.0
MAIN_FRONT = 5.0

# === COLUMNS — 7 per side, taller for 7m ceiling ===
NUM_COLS = 7
COL_H = 6.5
COL_R_BASE = 0.3
COL_R_TOP = 0.2
WALL_OFFSET = 0.5
SPACING = (MAIN_FRONT - MAIN_BACK) / (NUM_COLS + 1)

for side, x in [("L", -W/2 + WALL_OFFSET), ("R", W/2 - WALL_OFFSET)]:
    names = []
    for i in range(NUM_COLS):
        y = MAIN_BACK + SPACING * (i + 1)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=COL_R_BASE, radius2=COL_R_TOP, depth=COL_H, location=(x, y, COL_H/2))
        o = bpy.context.active_object
        o.name = f"Col_{side}_{i}"
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        names.append(o.name)

    # join
    bpy.ops.object.select_all(action='DESELECT')
    for n in names:
        bpy.data.objects[n].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[names[0]]
    bpy.ops.object.join()
    bpy.context.active_object.name = f"Columns_{side}"

# === STAGE FRAME — behind DJ, framing the screen ===
FRAME_W = 10.5
PILLAR_H = 6.0
FRAME_Y = MAIN_BACK + 0.8

# pillars
parts = []
for side, sx in [("L", -FRAME_W/2), ("R", FRAME_W/2)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(sx, FRAME_Y, PILLAR_H/2))
    o = bpy.context.active_object
    o.name = f"SF_{side}"
    o.scale = (0.5, 0.4, PILLAR_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o.name)

# lintel
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, FRAME_Y, PILLAR_H + 0.25))
o = bpy.context.active_object
o.name = "SF_Top"
o.scale = (FRAME_W + 0.5, 0.4, 0.5)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
parts.append(o.name)

bpy.ops.object.select_all(action='DESELECT')
for n in parts:
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[parts[0]]
bpy.ops.object.join()
bpy.context.active_object.name = "Stage_Frame"

# === TOTEMS — flanking the screen ===
TOTEM_X = 6.0
TOTEM_Y = MAIN_BACK + 0.8

for side, sign in [("L", -1), ("R", 1)]:
    x = sign * TOTEM_X
    tp = []
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.55, radius2=0.4, depth=2.2, location=(x, TOTEM_Y, 1.1))
    o = bpy.context.active_object
    o.name = f"TT_{side}_B"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    tp.append(o.name)

    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.4, radius2=0.22, depth=1.5, location=(x, TOTEM_Y, 2.95))
    o = bpy.context.active_object
    o.name = f"TT_{side}_M"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    tp.append(o.name)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.35, location=(x, TOTEM_Y, 3.95))
    o = bpy.context.active_object
    o.name = f"TT_{side}_T"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    tp.append(o.name)

    bpy.ops.object.select_all(action='DESELECT')
    for n in tp:
        bpy.data.objects[n].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[tp[0]]
    bpy.ops.object.join()
    bpy.context.active_object.name = f"Totem_{side}"

# === BACKDROP RELIEF — on the screen surface ===
RELIEF_Y = MAIN_BACK + 0.55
RELIEF_Z = 1.5 + 4.5/2  # center of screen

ring_names = []
for i, rad in enumerate([1.4, 0.95, 0.55]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=rad, depth=0.05, location=(0, RELIEF_Y, RELIEF_Z))
    o = bpy.context.active_object
    o.rotation_euler = (math.pi/2, 0, math.pi/8)
    o.name = f"Rel_{i}"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ring_names.append(o.name)

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.2, depth=0.08, location=(0, RELIEF_Y - 0.02, RELIEF_Z))
o = bpy.context.active_object
o.rotation_euler = (math.pi/2, 0, math.pi/8)
o.name = "Rel_C"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
ring_names.append("Rel_C")

for j in range(4):
    angle = j * (math.pi/4) + math.pi/8
    dx = math.cos(angle) * 1.2/2
    dz = math.sin(angle) * 1.2/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(dx, RELIEF_Y, RELIEF_Z + dz))
    o = bpy.context.active_object
    o.name = f"Rel_B{j}"
    o.scale = (1.2, 0.04, 0.03)
    o.rotation_euler = (0, -angle, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ring_names.append(o.name)

bpy.ops.object.select_all(action='DESELECT')
for n in ring_names:
    obj = bpy.data.objects.get(n)
    if obj:
        obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[ring_names[0]]
bpy.ops.object.join()
bpy.context.active_object.name = "Backdrop_Relief"

# === CEILING BEAMS — taller room, 6 beams ===
NUM_BEAMS = 6
BEAM_H = 0.35
BEAM_D = 0.4
SPACING_B = (MAIN_FRONT - MAIN_BACK) / (NUM_BEAMS + 1)

beam_names = []
for i in range(NUM_BEAMS):
    y = MAIN_BACK + SPACING_B * (i + 1)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, H - BEAM_H/2))
    o = bpy.context.active_object
    o.name = f"Beam_{i}"
    o.scale = (W, BEAM_D, BEAM_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    beam_names.append(o.name)

bpy.ops.object.select_all(action='DESELECT')
for n in beam_names:
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[beam_names[0]]
bpy.ops.object.join()
bpy.context.active_object.name = "Ceiling_Beams"

# === FLOOR FLOW GUIDES ===
import math
H_STRIP = 0.025
STRIP_W = 0.12
flow_names = []

# center line: entry to origin
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 6.5, H_STRIP/2))
o = bpy.context.active_object
o.name = "Flow_Entry"
o.scale = (STRIP_W, 7.0, H_STRIP)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
flow_names.append(o.name)

# center line: origin to stage
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.35, H_STRIP/2))
o = bpy.context.active_object
o.name = "Flow_Stage"
o.scale = (STRIP_W, 4.7, H_STRIP)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
flow_names.append(o.name)

# radial guides from origin
for i, angle in enumerate([math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]):
    length = 5.5
    cx = math.cos(angle) * length/2
    cy = math.sin(angle) * length/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, H_STRIP/2))
    o = bpy.context.active_object
    o.name = f"Flow_R{i}"
    o.scale = (length, STRIP_W, H_STRIP)
    o.rotation_euler = (0, 0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    flow_names.append(o.name)

bpy.ops.object.select_all(action='DESELECT')
for n in flow_names:
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[flow_names[0]]
bpy.ops.object.join()
bpy.context.active_object.name = "Floor_FlowGuides"

# report
identity = ["Columns_L", "Columns_R", "Stage_Frame", "Totem_L", "Totem_R", "Backdrop_Relief", "Ceiling_Beams", "Floor_FlowGuides"]
for name in identity:
    obj = bpy.data.objects.get(name)
    if obj:
        print(f"{name}: {len(obj.data.polygons)}p")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 6: MATERIALS
# ============================================================
print("\n--- applying materials ---")
r = execute_code(r"""
import bpy

def make_mat(name, base, rough=0.5, metal=0.0, emit_color=None, emit_str=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit_color:
        bsdf.inputs["Emission Color"].default_value = (*emit_color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit_str
    return mat

# create all materials
mats = {
    "DarkConcrete_Metal": make_mat("DarkConcrete_Metal", (0.055, 0.05, 0.06), 0.88, 0.05),
    "DarkWall_Metal": make_mat("DarkWall_Metal", (0.025, 0.025, 0.035), 0.95, 0.0),
    "DarkCeiling_Metal": make_mat("DarkCeiling_Metal", (0.015, 0.015, 0.018), 0.98, 0.0),
    "StageSurface_Metal": make_mat("StageSurface_Metal", (0.09, 0.07, 0.1), 0.5, 0.4),
    "StageEdge_Metal": make_mat("StageEdge_Metal", (0.04, 0.03, 0.05), 0.3, 0.85),
    "BoothMetal_Metal": make_mat("BoothMetal_Metal", (0.035, 0.035, 0.045), 0.3, 0.9),
    "Screen_Unlit": make_mat("Screen_Unlit", (0.08, 0.04, 0.12), 0.5, 0.0, (0.12, 0.06, 0.2), 2.5),
    "OriginSurface_Metal": make_mat("OriginSurface_Metal", (0.04, 0.04, 0.055), 0.4, 0.6),
    "OriginRing_Unlit": make_mat("OriginRing_Unlit", (0.18, 0.1, 0.3), 0.5, 0.0, (0.2, 0.12, 0.35), 5.0),
    "SpawnMarker_Unlit": make_mat("SpawnMarker_Unlit", (0.06, 0.08, 0.12), 0.5, 0.0, (0.08, 0.1, 0.16), 1.5),
    "ColumnStone_Metal": make_mat("ColumnStone_Metal", (0.065, 0.055, 0.075), 0.7, 0.25),
    "FrameMetal_Metal": make_mat("FrameMetal_Metal", (0.03, 0.025, 0.04), 0.25, 0.95),
    "ReliefGlow_Unlit": make_mat("ReliefGlow_Unlit", (0.14, 0.07, 0.22), 0.5, 0.0, (0.16, 0.08, 0.25), 5.0),
    "TotemStone_Metal": make_mat("TotemStone_Metal", (0.055, 0.045, 0.065), 0.55, 0.45),
    "BeamConcrete_Metal": make_mat("BeamConcrete_Metal", (0.035, 0.035, 0.04), 0.85, 0.1),
    "FlowGuide_Unlit": make_mat("FlowGuide_Unlit", (0.08, 0.06, 0.12), 0.5, 0.0, (0.1, 0.07, 0.16), 2.0),
    "Tier1_Metal": make_mat("Tier1_Metal", (0.045, 0.04, 0.055), 0.7, 0.3),
    "EntryCeiling_Metal": make_mat("EntryCeiling_Metal", (0.02, 0.02, 0.025), 0.95, 0.0),
}

# assign
assignments = {
    "Floor": "DarkConcrete_Metal",
    "Wall_Back": "DarkWall_Metal",
    "Wall_Left": "DarkWall_Metal",
    "Wall_Right": "DarkWall_Metal",
    "Wall_Front_L": "DarkWall_Metal",
    "Wall_Front_R": "DarkWall_Metal",
    "Wall_Entry_L": "DarkWall_Metal",
    "Wall_Entry_R": "DarkWall_Metal",
    "Ceiling_Main": "DarkCeiling_Metal",
    "Ceiling_Entry": "EntryCeiling_Metal",
    "Stage_Platform": "StageSurface_Metal",
    "Stage_Edge": "StageEdge_Metal",
    "DJ_Booth": "BoothMetal_Metal",
    "Stage_Screen": "Screen_Unlit",
    "DanceFloor_Tier1": "Tier1_Metal",
    "Origin_Focal": "OriginSurface_Metal",
    "Origin_Ring": "OriginRing_Unlit",
    "Spawn_Marker": "SpawnMarker_Unlit",
    "Columns_L": "ColumnStone_Metal",
    "Columns_R": "ColumnStone_Metal",
    "Stage_Frame": "FrameMetal_Metal",
    "Totem_L": "TotemStone_Metal",
    "Totem_R": "TotemStone_Metal",
    "Backdrop_Relief": "ReliefGlow_Unlit",
    "Ceiling_Beams": "BeamConcrete_Metal",
    "Floor_FlowGuides": "FlowGuide_Unlit",
}

for obj_name, mat_name in assignments.items():
    obj = bpy.data.objects.get(obj_name)
    mat = bpy.data.materials.get(mat_name)
    if obj and mat:
        obj.data.materials.clear()
        obj.data.materials.append(mat)

# purge unused materials
used = set()
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                used.add(slot.material.name)
for mat in list(bpy.data.materials):
    if mat.name not in used:
        bpy.data.materials.remove(mat)

print(f"materials assigned: {len(used)} unique")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 7: LIGHTING
# ============================================================
print("\n--- setting up lighting ---")
r = execute_code(r"""
import bpy

H = 7.0

# remove any existing lights
for obj in [o for o in bpy.data.objects if o.type == "LIGHT"]:
    bpy.data.objects.remove(obj, do_unlink=True)

lights = [
    # stage — warm, focused
    {"name": "Light_Stage", "loc": (0, -7.5, 6.0), "energy": 1200, "color": (1.0, 0.8, 0.6), "size": 1.0},
    # screen backwash
    {"name": "Light_ScreenWash", "loc": (0, -9.0, 4.0), "energy": 200, "color": (0.3, 0.15, 0.5), "size": 2.5},
    # origin focal
    {"name": "Light_Origin", "loc": (0, 0, 6.5), "energy": 500, "color": (0.5, 0.6, 1.0), "size": 2.0},
    # fill — dim ambient
    {"name": "Light_Fill", "loc": (0, 3.0, 5.0), "energy": 80, "color": (0.4, 0.35, 0.5), "size": 8.0},
    # left accent
    {"name": "Light_Left", "loc": (-8.0, -3.0, 5.5), "energy": 250, "color": (0.6, 0.25, 0.9), "size": 2.0},
    # right accent
    {"name": "Light_Right", "loc": (8.0, -3.0, 5.5), "energy": 250, "color": (0.6, 0.25, 0.9), "size": 2.0},
    # column wash left
    {"name": "Light_ColWash_L", "loc": (-9.0, -2.0, 1.5), "energy": 100, "color": (0.9, 0.6, 0.4), "size": 3.5},
    # column wash right
    {"name": "Light_ColWash_R", "loc": (9.0, -2.0, 1.5), "energy": 100, "color": (0.9, 0.6, 0.4), "size": 3.5},
    # entry corridor — subtle warm guide
    {"name": "Light_Entry", "loc": (0, 7.5, 3.0), "energy": 60, "color": (0.8, 0.6, 0.5), "size": 3.0},
    # tier 1 dance floor wash
    {"name": "Light_Tier1", "loc": (0, -3.5, 5.0), "energy": 150, "color": (0.5, 0.4, 0.8), "size": 2.0},
]

for cfg in lights:
    bpy.ops.object.light_add(type='POINT', location=cfg["loc"])
    l = bpy.context.active_object
    l.name = cfg["name"]
    l.data.energy = cfg["energy"]
    l.data.color = cfg["color"]
    l.data.shadow_soft_size = cfg["size"]

# camera
bpy.ops.object.camera_add(location=(0, 8.0, 2.0))
cam = bpy.context.active_object
cam.name = "Camera_Main"
import math
cam.rotation_euler = (math.radians(85), 0, math.radians(180))
bpy.context.scene.camera = cam

# world background
scene = bpy.context.scene
if not scene.world:
    scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.005, 0.005, 0.008, 1.0)
    bg.inputs["Strength"].default_value = 0.1

light_count = len([o for o in bpy.data.objects if o.type == "LIGHT"])
print(f"lights placed: {light_count}")
""")
print(r.get("result", {}).get("result", r))

# ============================================================
# STEP 8: VALIDATE + EXPORT
# ============================================================
print("\n--- validating ---")
r = execute_code(r"""
import bpy, os

# apply transforms
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(False)

# validate
errors = []
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type != 'MESH':
        continue
    p = len(obj.data.polygons)
    t = sum(len(f.vertices) - 2 for f in obj.data.polygons)
    m = len(obj.data.materials)
    s = "OK"
    if p > 50000:
        errors.append(f"{obj.name}: {p}p > 50000")
        s = "OVER"
    if m > 2:
        errors.append(f"{obj.name}: {m}m > 2")
        s = "OVER"
    print(f"  {obj.name}: {p}p {t}t {m}m — {s}")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
tp = sum(len(o.data.polygons) for o in meshes)
tt = sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes)
lights = len([o for o in bpy.data.objects if o.type == 'LIGHT'])

if errors:
    print(f"\nFAILED: {len(errors)} errors")
else:
    print(f"\nPASSED — {len(meshes)} meshes, {tp} polys, {tt} tris, {lights} lights")

# export
export_dir = "/Users/chanceneihouse/GitHub/world-builder-agent/world/fbx"
os.makedirs(export_dir, exist_ok=True)
path = os.path.join(export_dir, "pg_origin_club_final.fbx")
bpy.ops.export_scene.fbx(
    filepath=path, use_selection=False,
    apply_scale_options='FBX_SCALE_ALL', apply_unit_scale=True,
    bake_space_transform=True, mesh_smooth_type='FACE',
    use_mesh_modifiers=True, add_leaf_bones=False,
    path_mode='COPY', embed_textures=True,
    object_types={'MESH', 'LIGHT', 'CAMERA'},
)
size = os.path.getsize(path)
print(f"\nexported: {path} ({size/1024:.1f} kb)")

bpy.ops.wm.save_as_mainfile(filepath="/Users/chanceneihouse/GitHub/world-builder-agent/world/pg_origin_club.blend")
print("blend saved")
""")
print(r.get("result", {}).get("result", r))
