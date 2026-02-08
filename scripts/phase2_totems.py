"""phase 2: add symmetrical sculptural totems flanking the stage."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code
import json

CODE = r"""
import bpy
import math

# === SCULPTURAL TOTEMS ===
# two symmetrical abstract monoliths flanking the stage
# stacked geometric primitives — primordial feel
# each totem: base octagon + tapered middle + sphere-like top

STAGE_FRAME_X = 4.0  # half-width of stage frame
TOTEM_X_OFFSET = 5.2  # just outside stage frame
TOTEM_Y = -3.2  # aligned with stage area
TOTEM_BASE_H = 1.8
TOTEM_MID_H = 1.2
TOTEM_TOP_R = 0.3

created_names = []

for side, sign in [("L", -1), ("R", 1)]:
    x = sign * TOTEM_X_OFFSET
    parts = []

    # base — tapered hexagonal column
    bpy.ops.mesh.primitive_cone_add(
        vertices=6,
        radius1=0.5,
        radius2=0.35,
        depth=TOTEM_BASE_H,
        location=(x, TOTEM_Y, TOTEM_BASE_H / 2)
    )
    base = bpy.context.active_object
    base.name = f"Totem_{side}_Base"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(base.name)

    # middle — narrower octagonal section
    bpy.ops.mesh.primitive_cone_add(
        vertices=8,
        radius1=0.35,
        radius2=0.2,
        depth=TOTEM_MID_H,
        location=(x, TOTEM_Y, TOTEM_BASE_H + TOTEM_MID_H / 2)
    )
    mid = bpy.context.active_object
    mid.name = f"Totem_{side}_Mid"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(mid.name)

    # top — icosphere cap (low subdivision)
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=TOTEM_TOP_R,
        location=(x, TOTEM_Y, TOTEM_BASE_H + TOTEM_MID_H + TOTEM_TOP_R * 0.7)
    )
    top = bpy.context.active_object
    top.name = f"Totem_{side}_Top"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(top.name)

    # join into single totem mesh
    bpy.ops.object.select_all(action='DESELECT')
    for name in parts:
        bpy.data.objects[name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[parts[0]]
    bpy.ops.object.join()
    totem = bpy.context.active_object
    totem.name = f"Totem_{side}"
    created_names.append(totem.name)

for name in created_names:
    obj = bpy.data.objects[name]
    polys = len(obj.data.polygons)
    print(f"{name}: {polys} polys")
"""

result = execute_code(CODE)
print(json.dumps(result, indent=2))
