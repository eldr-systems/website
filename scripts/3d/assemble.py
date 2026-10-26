# scripts/3d/blender.sh --python scripts/3d/assemble.py
#
# Builds 3d-models/keep.blend from the meshes step_to_mesh.py writes: The Keep
# closed, centred on the origin, Z up, case length along X. Positions are a first
# guess; correct them by hand in keep.blend and the render scripts pick that up.
import math, os
import bpy
from mathutils import Matrix, Vector

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "3d-models")
MESHES = os.path.join(ROOT, "meshes")

# Brand tokens from assets/css/main.css, as linear RGB for Blender.
def srgb(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

def material(name, hex_, roughness, metallic=0.0):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = srgb(hex_)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    m.diffuse_color = srgb(hex_)  # workbench / viewport colour
    return m

def load(name):
    bpy.ops.wm.stl_import(filepath=os.path.join(MESHES, name + ".stl"))
    o = bpy.context.selected_objects[0]
    o.name = o.data.name = name
    return o

def bounds(o):
    # From the vertices: bound_box goes stale after mesh.transform().
    vs = [o.matrix_world @ v.co for v in o.data.vertices]
    return (Vector([min(v[i] for v in vs) for i in range(3)]),
            Vector([max(v[i] for v in vs) for i in range(3)]))

def bake(o, matrix):
    o.data.transform(matrix)
    o.data.update()

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 0.001  # 1 unit = 1 mm

case_mat = material("case", "#F4F1EA", 0.55)   # bone: printed PLA
board_mat = material("board", "#14161A", 0.4)  # ink: PCB and parts
sensor_mat = material("sensor", "#5B6B7A", 0.4)  # slate

# Base: open top, floor on z=0, centred on X/Y.
base = load("case-base")
lo, hi = bounds(base)
bake(base, Matrix.Translation(-(lo + hi) / 2 * Vector((1, 1, 0)) - Vector((0, 0, lo.z))))
base_hi = bounds(base)[1]

# Lid: printed upside down. Flip about X so its sensor chamber stays at -X with
# the base's, then seat it on the base rim.
top = load("case-top")
bake(top, Matrix.Rotation(math.pi, 4, "X"))
lo, hi = bounds(top)
bake(top, Matrix.Translation(-(lo + hi) / 2 * Vector((1, 1, 0)) + Vector((0, 0, base_hi.z - lo.z))))

# Board: exported standing on edge with the 18650 holder towards +Y. Lay it flat,
# holder down on the case floor and header pins up, pushed to the +X end away from the sensor chamber.
board = load("lilygo")
bake(board, Matrix.Rotation(math.pi / 2, 4, "X"))
lo, hi = bounds(board)
wall, floor = 3.0, 3.0
bake(board, Matrix.Translation(Vector((
    base_hi.x - wall - hi.x,
    -(lo.y + hi.y) / 2,
    floor - lo.z))))
dec = board.modifiers.new("decimate", "DECIMATE")
dec.ratio = 0.3
bpy.context.view_layer.objects.active = board
bpy.ops.object.modifier_apply(modifier=dec.name)

# Sensor: a vertical plate in the -X chamber, pins pointing +X towards the board.
sensor = load("sensor")
bake(sensor, Matrix.Rotation(-math.pi / 2, 4, "Z"))
lo, hi = bounds(sensor)
bake(sensor, Matrix.Translation(Vector((
    bounds(base)[0].x + wall + 4 - lo.x,
    -(lo.y + hi.y) / 2,
    floor + 8 - lo.z))))

for o, m in ((base, case_mat), (top, case_mat), (board, board_mat), (sensor, sensor_mat)):
    o.data.materials.append(m)
    # Origin at the part's centre, so the explode offsets read as plain moves.
    lo, hi = bounds(o)
    c = (lo + hi) / 2
    o.data.transform(Matrix.Translation(-c))
    o.location = c
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.shade_auto_smooth(angle=math.radians(30))

for o in (base, top, board, sensor):
    lo, hi = bounds(o)
    print(f"PART {o.name:10} {len(o.data.polygons):7} faces  "
          f"min {tuple(round(x, 1) for x in lo)}  max {tuple(round(x, 1) for x in hi)}")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "keep.blend"))
