"""full scene audit before Horizon import."""
import sys
sys.path.insert(0, "/Users/chanceneihouse/GitHub/world-builder-agent")
from blender_cmd import execute_code

CODE = r"""
import bpy

print('=== FULL SCENE AUDIT ===')
print()

# 1. Object inventory
print('--- MESHES ---')
meshes = sorted([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: o.name)
for obj in meshes:
    p = len(obj.data.polygons)
    t = sum(len(f.vertices)-2 for f in obj.data.polygons)
    m = len(obj.data.materials)
    mat_name = obj.data.materials[0].name if obj.data.materials else 'NONE'
    loc = [round(v,2) for v in obj.location]
    scl = [round(v,2) for v in obj.scale]
    rot = [round(v,2) for v in obj.rotation_euler]

    issues = []
    if m == 0:
        issues.append('NO MATERIAL')
    if m > 2:
        issues.append('TOO MANY MATS (%d)' % m)
    if p > 50000:
        issues.append('OVER POLY LIMIT (%d)' % p)
    if any(s != 1.0 for s in scl):
        issues.append('UNAPPLIED SCALE %s' % scl)
    if any(r != 0.0 for r in rot):
        issues.append('UNAPPLIED ROT %s' % rot)
    if '.' in obj.name and obj.name.split('.')[-1].isdigit():
        issues.append('DUPLICATE NAME')

    if m > 0:
        for slot in obj.material_slots:
            if slot.material:
                mn = slot.material.name
                valid_suffixes = ['_Metal', '_Unlit', '_Blend', '_Transparent', '_Masked', '_VXC', '_VXM', '_UIO']
                has_suffix = any(mn.endswith(s) for s in valid_suffixes)
                if not has_suffix:
                    issues.append('BAD MAT SUFFIX: %s' % mn)
                bad_chars = ['-', '.', ',', '/', '*', '$', '&']
                for c in bad_chars:
                    if c in mn:
                        issues.append('BAD CHAR in mat: %s' % mn)
                        break

    status = 'OK' if not issues else ' | '.join(issues)
    print('  %s: %dp %dt mat=%s loc=%s [%s]' % (obj.name, p, t, mat_name, loc, status))

print()
print('--- LIGHTS ---')
lights = sorted([o for o in bpy.data.objects if o.type == 'LIGHT'], key=lambda o: o.name)
for obj in lights:
    c = tuple(round(v,2) for v in obj.data.color)
    loc = [round(v,1) for v in obj.location]
    print('  %s: type=%s energy=%s color=%s loc=%s' % (obj.name, obj.data.type, obj.data.energy, c, loc))

print()
print('--- CAMERAS ---')
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        loc = [round(v,1) for v in obj.location]
        print('  %s: loc=%s' % (obj.name, loc))

print()
print('--- MATERIALS ---')
used_mats = set()
for obj in meshes:
    for slot in obj.material_slots:
        if slot.material:
            used_mats.add(slot.material.name)

for mat in sorted(bpy.data.materials, key=lambda m: m.name):
    status = 'USED' if mat.name in used_mats else 'ORPHAN'
    bsdf = None
    if mat.use_nodes:
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf = node
                break
    if bsdf:
        bc = tuple(round(v,3) for v in bsdf.inputs['Base Color'].default_value[:3])
        rough = round(bsdf.inputs['Roughness'].default_value, 3)
        metal = round(bsdf.inputs['Metallic'].default_value, 3)
        emit_str = round(bsdf.inputs['Emission Strength'].default_value, 3)
        print('  %s: base=%s rough=%s metal=%s emit=%s [%s]' % (mat.name, bc, rough, metal, emit_str, status))
    else:
        print('  %s: [no BSDF] [%s]' % (mat.name, status))

print()
print('--- ORPHAN DATA ---')
orphan_meshes = [m for m in bpy.data.meshes if m.users == 0]
orphan_mats = [m for m in bpy.data.materials if m.name not in used_mats]
print('  orphan meshes: %d' % len(orphan_meshes))
print('  orphan materials: %d' % len(orphan_mats))
for m in orphan_mats:
    print('    - %s' % m.name)

print()
print('--- SCENE BOUNDS ---')
import mathutils
all_coords = []
for obj in meshes:
    for v in obj.data.vertices:
        world_co = obj.matrix_world @ v.co
        all_coords.append(world_co)
if all_coords:
    xs = [c.x for c in all_coords]
    ys = [c.y for c in all_coords]
    zs = [c.z for c in all_coords]
    print('  X: %.1f to %.1f (width: %.1fm)' % (min(xs), max(xs), max(xs)-min(xs)))
    print('  Y: %.1f to %.1f (depth: %.1fm)' % (min(ys), max(ys), max(ys)-min(ys)))
    print('  Z: %.1f to %.1f (height: %.1fm)' % (min(zs), max(zs), max(zs)-min(zs)))

print()
print('--- TOTALS ---')
tp = sum(len(o.data.polygons) for o in meshes)
tt = sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes)
print('  meshes: %d' % len(meshes))
print('  polys: %d' % tp)
print('  tris: %d' % tt)
print('  materials (used): %d' % len(used_mats))
print('  lights: %d' % len(lights))

print()
print('--- HORIZON IMPORT CHECKLIST ---')
errors = 0
warnings = 0

# check all objects have materials
no_mat = [o.name for o in meshes if not o.data.materials]
if no_mat:
    print('  ERROR: objects with no material: %s' % no_mat)
    errors += 1

# check material suffixes
for mat in bpy.data.materials:
    if mat.name in used_mats:
        valid = ['_Metal', '_Unlit', '_Blend', '_Transparent', '_Masked', '_VXC', '_VXM', '_UIO']
        if not any(mat.name.endswith(s) for s in valid):
            print('  ERROR: material missing Horizon suffix: %s' % mat.name)
            errors += 1

# check for unapplied transforms
for obj in meshes:
    if any(round(s,2) != 1.0 for s in obj.scale):
        print('  ERROR: unapplied scale on %s: %s' % (obj.name, [round(v,2) for v in obj.scale]))
        errors += 1
    if any(round(r,2) != 0.0 for r in obj.rotation_euler):
        print('  WARNING: unapplied rotation on %s' % obj.name)
        warnings += 1

# check for duplicate names
names = [o.name for o in meshes]
for n in names:
    if '.' in n and n.split('.')[-1].isdigit():
        print('  ERROR: duplicate object name: %s' % n)
        errors += 1

# check poly limits
for obj in meshes:
    if len(obj.data.polygons) > 50000:
        print('  ERROR: %s exceeds 50k poly limit (%d)' % (obj.name, len(obj.data.polygons)))
        errors += 1

# check materials per object
for obj in meshes:
    if len(obj.data.materials) > 2:
        print('  ERROR: %s has %d materials (max 2)' % (obj.name, len(obj.data.materials)))
        errors += 1

if errors == 0 and warnings == 0:
    print('  ALL CHECKS PASSED')
elif errors == 0:
    print('  PASSED with %d warnings' % warnings)
else:
    print('  FAILED: %d errors, %d warnings' % (errors, warnings))
"""

result = execute_code(CODE)
print(result.get("result", {}).get("result", result))
