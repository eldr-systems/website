# scripts/3d/blender.sh 3d-models/keep.blend --python scripts/3d/render_assembly.py -- OUT_DIR shaded|lineart|strokes [FRAME ...]
#
# The Keep assembling itself, seen from above: the parts lie on the table (board
# upside down, lid beside the box, sensor on its back), then the board flips
# onto its posts, the lid flips over so the sensor can slide into the pocket on
# its ceiling, and the lid flips back and closes with the sensor inside. It then plays back to the table, so the
# PNG frames in OUT_DIR loop without a jump. "shaded" is the studio render (B),
# "lineart" the ink-on-bone drawing (A). Give frame numbers to render stills.
# "strokes" renders nothing: it writes the drawing's strokes for the way in only
# (no hold, no playback), sampled every few frames and projected through each
# frame's camera, to OUT_DIR/strokes.json for compose_flipbook.py.
import math, os, sys
import bpy
from mathutils import Euler, Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import studio

args = sys.argv[sys.argv.index("--") + 1:]
out_dir, style, frames = args[0], args[1], [int(f) for f in args[2:]]

scene = bpy.context.scene
parts = {n: bpy.data.objects[n] for n in ("case-base", "case-top", "lilygo", "sensor")}
final = {n: o.location.copy() for n, o in parts.items()}

# Where each part lies on the table (x, y in mm, box at the origin) and how it is
# turned. Heights are worked out so each part rests on the table.
TABLE = {
    "case-base": ((0, 0), (0, 0, 0)),
    "case-top":  ((0, 74), (0, 0, 0)),                   # beside the box, right way up
    "lilygo":    ((8, -68), (math.pi, 0, 0)),            # upside down: pins down
    "sensor":    ((-104, -6), (math.pi, 0, 0)),          # on its back: pins up
}

def resting(name):
    (x, y), rot = TABLE[name]
    m = Euler(rot).to_matrix()
    lowest = min((m @ v.co).z for v in parts[name].data.vertices)
    return Vector((x, y, -lowest)), Euler(rot)

# The sequence, as stops per part: (frame, location, rotation). Bezier keys ease
# in and out of every stop, so each part moves pick-and-place style: lift, carry
# (turning on the way), lower.
UP = Euler((0, 0, 0))
keys = {}
def stops(name, *seq):
    keys[name] = seq

table = {n: resting(n) for n in parts}
board_lift = 52  # mm above the posts when the board is carried over

stops("case-base", (1, final["case-base"], UP))
stops("lilygo",
      (30, *table["lilygo"]),
      (50, table["lilygo"][0] + Vector((0, 0, 60)), table["lilygo"][1]),
      (88, final["lilygo"] + Vector((0, 0, board_lift)), UP),
      (108, final["lilygo"], UP))

# The sensor's pocket is on the lid's ceiling, which faces the table. So the lid
# lifts and turns over where it lies (cavity up, clear of the box), the sensor
# comes over and slides into the pocket from the middle of the lid, and the lid
# turns back with it inside and closes.
FLIPPED = Euler((math.pi, 0, 0))
hover = table["case-top"][0] + Vector((0, 0, 62))
lid_hover = Matrix.LocRotScale(hover, FLIPPED, None)
def in_hovering_lid(loc):
    """Where a point of the closed Keep is while the lid hovers turned over."""
    return lid_hover @ Matrix.Translation(final["case-top"]).inverted() @ loc
seated = in_hovering_lid(final["sensor"])
SLIDE = Vector((26, 0, 0))  # the slot opens towards +X: slide in along -X
stops("case-top",
      (112, *table["case-top"]),
      (134, hover, FLIPPED),
      (180, hover, FLIPPED),
      (198, hover + Vector((0, 0, 6)), UP),
      (216, final["case-top"] + Vector((0, 0, 40)), UP),
      (236, final["case-top"], UP))
stops("sensor",
      (118, *table["sensor"]),
      (134, table["sensor"][0] + Vector((0, 0, 60)), FLIPPED),
      (152, seated + SLIDE + Vector((0, 0, 30)), FLIPPED),  # above the open lid
      (162, seated + SLIDE, FLIPPED),
      (176, seated, FLIPPED))
SEATED = 176
HOLD = 266  # closed until here, then everything plays back

def keyframe(o, frame, loc, rot):
    o.location, o.rotation_euler = loc, rot
    o.keyframe_insert("location", frame=frame)
    o.keyframe_insert("rotation_euler", frame=frame)

for name, seq in keys.items():
    o = parts[name]
    seq = [(1, *seq[0][1:])] + list(seq) + [(HOLD, *seq[-1][1:])]
    for frame, loc, rot in seq:
        keyframe(o, frame, loc, rot)
        keyframe(o, 2 * HOLD - frame, loc, rot)  # the way back, mirrored

# Once seated, the sensor rides with the lid: a Child Of constraint, switched on
# the frame after it slides home, with the lid's hovering pose as its inverse so
# nothing jumps.
ride = parts["sensor"].constraints.new("CHILD_OF")
ride.target = parts["case-top"]
ride.inverse_matrix = lid_hover.inverted()
for frame, on in ((1, 0), (SEATED, 0), (SEATED + 1, 1), (HOLD, 1)):
    ride.influence = on
    for f in (frame, 2 * HOLD - frame):
        ride.keyframe_insert("influence", frame=f)

# Camera: straight down over the table, tilting to a three-quarter view while the
# parts lift, settling on the closed product. Keyed densely along an arc (not a
# straight line, which would dip towards the parts) and aimed by a Track To.
TOP = (Vector((-14, 2, 0)), Vector((0, -0.1, 1)).normalized(), 640)
THREE_Q = (Vector((0, 0, 44)), Vector((0.85, -1.0, 0.62)).normalized(), 470)
TILT_FROM, TILT_TO = 34, 236

target = bpy.data.objects.new("target", None)
scene.collection.objects.link(target)
cam = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
scene.collection.objects.link(cam)
scene.camera = cam
cam.data.lens = 70
cam.data.clip_end = 5000
if style in ("lineart", "strokes"):
    cam.data.type = "ORTHO"  # a technical drawing has no perspective
track = cam.constraints.new("TRACK_TO")
track.target, track.track_axis, track.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"

def smooth(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)

# While the lid hovers turned over beside the box and the sensor slides in, the
# camera leans towards it and pulls back, so that happens in frame.
LID_FOCUS = (108, 138, 180, 206)  # ease in from, fully on, ease out from, off
def lid_focus(frame):
    a, b, c, d = LID_FOCUS
    return smooth((frame - a) / (b - a)) * (1 - smooth((frame - c) / (d - c)))

def camera_key(frame, t):
    s = smooth(t)
    aim = TOP[0].lerp(THREE_Q[0], s) + Vector((0, 40, 24)) * lid_focus(frame)
    direction = TOP[1].slerp(THREE_Q[1], s)
    distance = TOP[2] + (THREE_Q[2] - TOP[2]) * s + 70 * lid_focus(frame)
    target.location = aim
    cam.location = aim + direction * distance
    cam.data.ortho_scale = distance * 36 / 70  # same framing as the 70 mm lens
    for f in (frame, 2 * HOLD - frame):
        target.keyframe_insert("location", frame=f)
        cam.keyframe_insert("location", frame=f)
        cam.data.keyframe_insert("ortho_scale", frame=f)

camera_key(1, 0)
for frame in range(TILT_FROM, TILT_TO + 1, 4):
    camera_key(frame, (frame - TILT_FROM) / (TILT_TO - TILT_FROM))
camera_key(HOLD, 1)

# Frame 2*HOLD-1 is frame 1 again: stop one short so the loop has no double frame.
studio.output(scene, out_dir, 1, 2 * HOLD - 2)
if style in ("lineart", "strokes"):
    lines = studio.lineart(scene, list(parts.values()), radius=0.32)
else:
    studio.shaded(scene)

if style == "strokes":
    import json
    from bpy_extras.object_utils import world_to_camera_view
    W, H = scene.render.resolution_x, scene.render.resolution_y
    out = {"width": W, "height": H, "frames": []}
    # From the first lift to the lid closing; the scroll position does the rest.
    for f in frames or range(26, 239, 3):
        scene.frame_set(f)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        gp = lines.evaluated_get(depsgraph).data
        drawing = gp.layers["lines"].current_frame().drawing
        strokes = []
        for stroke in drawing.strokes:
            pts = []
            for p in stroke.points:
                v = world_to_camera_view(scene, cam, lines.matrix_world @ p.position)
                pt = (round(v.x * W), round((1 - v.y) * H))
                if not pts or pt != pts[-1]:
                    pts.append(pt)
            if len(pts) > 1:
                strokes.append(pts)
        out["frames"].append({"frame": f, "strokes": strokes})
        print("FRAME", f, len(strokes), sum(map(len, strokes)))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "strokes.json"), "w") as fh:
        json.dump(out, fh)
elif frames:
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(out_dir, f"still-{f:03}")
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
