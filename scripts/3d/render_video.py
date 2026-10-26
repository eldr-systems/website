# scripts/3d/blender.sh 3d-models/keep.blend --python scripts/3d/render_video.py -- OUT_DIR [FRAME ...]
#
# Option B: The Keep bursting apart and closing again, as a seamless loop of PNG
# frames in OUT_DIR (encode_video.sh turns them into webm/mp4). Give frame numbers
# to render only those, as stills for checking the framing.
import math, os, sys
import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explode import OFFSETS, WAYPOINTS, place_camera

args = sys.argv[sys.argv.index("--") + 1:]
out_dir, frames = args[0], [int(f) for f in args[1:]]

FPS = 30
# closed hold, burst, open hold, close, closed hold: 160 frames, ~5.3 s.
CLOSED, OPEN_AT, OPEN_UNTIL, CLOSED_AT, END = 1, 45, 95, 139, 160

scene = bpy.context.scene

def srgb(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

# The case in the site's rule tone: bone-on-bone would vanish against the page.
bpy.data.materials["case"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb("#C9C3B6")

# Burst keyframes. Bezier keys with auto-clamped handles ease in and out of every
# stop, so a part with waypoints moves leg by leg. The lid leaves first and
# returns last; the sensor leaves last and returns first.
STAGGER = {"case-top": -6, "lilygo": 0, "sensor": 6, "case-base": 0}
BURST, CLOSE = 25, 44  # frames for the whole way out, and the whole way back
BURST_START = OPEN_AT - BURST
for name, offset in OFFSETS.items():
    o = bpy.data.objects[name]
    home, s = o.location.copy(), STAGGER[name]
    stops = [home] + [home + w for w in WAYPOINTS.get(name, [])] + [home + offset]
    legs = len(stops) - 1
    # Out: each extra leg gets its own time rather than squeezing the first. Back:
    # a multi-leg part hurries, so it is home before the lid comes down on it.
    out_len, back_len = BURST * (1 + 0.45 * (legs - 1)), CLOSE * (1 - 0.18 * (legs - 1))
    keys = [(CLOSED, home)]
    keys += [(BURST_START + s + out_len * i / legs, p) for i, p in enumerate(stops)]
    keys += [(OPEN_UNTIL - s + back_len * i / legs, p) for i, p in enumerate(reversed(stops))]
    keys += [(END, home)]
    for frame, loc in keys:
        o.location = loc
        o.keyframe_insert("location", frame=frame)
    o.location = home

# A slow sway of the whole view, back where it started at the loop seam.
pivot = bpy.data.objects.new("pivot", None)
scene.collection.objects.link(pivot)
cam = place_camera(scene)
cam.parent = pivot
for frame, angle in ((CLOSED, -8), ((CLOSED + END) // 2, 8), (END, -8)):
    pivot.rotation_euler = (0, 0, math.radians(angle))
    pivot.keyframe_insert("rotation_euler", frame=frame)

# Ground: bone, wide enough to fill the frame, so the background is the floor
# and the parts cast soft contact shadows on it.
bpy.ops.mesh.primitive_plane_add(size=4000)
ground = bpy.context.object
gm = bpy.data.materials.new("ground")
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb("#F4F1EA")
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
ground.data.materials.append(gm)

world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = srgb("#F4F1EA")
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6

def light(name, kind, energy, location, size):
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    if kind == "AREA":
        d.size = size
    else:
        d.angle = math.radians(size)
    o = bpy.data.objects.new(name, d)
    scene.collection.objects.link(o)
    o.location = location
    o.rotation_euler = (-Vector(location)).to_track_quat("-Z", "Y").to_euler()
    return o

light("key", "SUN", 3.2, (-200, -260, 420), 8)
light("fill", "AREA", 1.6e6, (420, -160, 200), 300)
light("rim", "AREA", 1.0e6, (-120, 400, 260), 250)

scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 1440, 1080
scene.render.fps = FPS
scene.frame_start, scene.frame_end = CLOSED, END - 1  # END == CLOSED: loop seam
scene.view_settings.view_transform = "Standard"  # keep brand colours exact
scene.view_settings.exposure = -0.7
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(out_dir, "f")

if frames:
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(out_dir, f"still-{f:03}")
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
