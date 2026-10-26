# scripts/3d/blender.sh --python scripts/3d/assemble.py
#
# Builds 3d-models/keep.blend from the meshes step_to_mesh.py writes: The Keep
# closed, centred on the origin, Z up, case length along X. Every part is placed
# from its CAD: the board on its screw posts, the sensor in the lid's pocket.
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

# Case features, read off the FreeCAD sketches in casing/*.FCStd. The base's own
# coordinates run x 0..131, y -52..0, floor at z=0; centring it puts it here:
BASE_TO_WORLD = Matrix.Translation((-65.5, 26, 0))
POST_CENTRE = BASE_TO_WORLD @ Vector((65.5, -26, 30))  # Sketch002/Pad002: four
#   board posts at x 12/119, y -12/-40, rising to z=30 (5 floor + 25)
# The big end-wall slot (Sketch003, x=0, z 30-40) keeps the case off the board's
# PCB antenna; the small round hole (Sketch007) is in the opposite end, x=131.

# The lid is printed upside down (z=0 is its outer top face, 27.5 tall). Flipped
# about X and centred, it sits on the base rim:
LID_TO_WORLD = Matrix.Translation((-1.6, 4.7, 72.5)) @ Matrix.Rotation(math.pi, 4, "X")
# Sensor pocket on the lid's ceiling (Sketch006/007): a block x -50.9..-30.9 with
# a slot through it, y -3.8..13.2, z 5..8. Its open face towards the middle of
# the lid, the slot's centre line, and its floor (z=8, away from the ceiling):
SLOT_FACE = LID_TO_WORLD @ Vector((-30.9, 4.7, 8))

def place(o, rotation, anchor, target):
    """Rotate o's mesh, then move it so the point anchor (in the mesh's own
    coordinates, before rotating) lands on target."""
    bake(o, rotation)
    bake(o, Matrix.Translation(target - rotation @ anchor))

base = load("case-base")
bake(base, BASE_TO_WORLD)
top = load("case-top")
bake(top, LID_TO_WORLD)

# Board, in the STEP's coordinates: PCB in the XZ plane, underside at y=105.9,
# 18650 holder towards -Y, mounting holes at x -60.0/46.9 and z 14.3/43.5, and
# the ESP32-WROVER's PCB antenna at the +X end. Battery down (-Y to -Z), and
# turned end for end so the antenna faces the big slot at -X; the holes' centre
# lands on the posts' centre, the underside on the post tops.
board = load("lilygo")
place(board, Matrix.Rotation(math.pi, 4, "Z") @ Matrix.Rotation(math.pi / 2, 4, "X"),
      Vector(((-60.0 + 46.9) / 2, 105.9, (14.3 + 43.5) / 2)), POST_CENTRE)
dec = board.modifiers.new("decimate", "DECIMATE")
dec.ratio = 0.3
bpy.context.view_layer.objects.active = board
bpy.ops.object.modifier_apply(modifier=dec.name)

# Sensor, in the STEP's coordinates: 15 x 15 plate in the XZ plane, PCB y 0..1.6
# with the chips on -Y, a straight header along the z=0..3 edge, pins out of +Y.
# It lies flat in the lid's slot, chips up towards the ceiling, pins hanging
# down towards the board, header edge just out of the slot's open face (towards
# the small-hole end, as the designer asked); the sensing end sits at the vents.
sensor = load("sensor")
place(sensor, Matrix(((0, 0, -1), (1, 0, 0), (0, -1, 0))).to_4x4(),  # x->y, y->-z, z->-x
      Vector((7.5, 1.6, 3.0)), SLOT_FACE)

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
