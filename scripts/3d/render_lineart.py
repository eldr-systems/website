# scripts/3d/blender.sh 3d-models/keep.blend --python scripts/3d/render_lineart.py -- OUT_DIR
#
# Option A, the Blender half: each part of The Keep in its exploded pose, drawn as
# Line Art (OUT_DIR/<part>.json, polylines in SVG pixels) plus a flat silhouette mask (OUT_DIR/<part>.png),
# and OUT_DIR/parts.json with each part's travel in SVG pixels. The camera is
# orthographic, so a part's 3D offset is one fixed 2D translate on the page.
# compose_lineart.py turns these into the site's SVG.
import json, math, os, sys
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explode import OFFSETS, WAYPOINTS, place_camera

out_dir = sys.argv[sys.argv.index("--") + 1]
os.makedirs(out_dir, exist_ok=True)

W, H, ORTHO = 1200, 900, 300
# Line weight per part, in px at 1200 wide: the case reads as the outline, the
# board's dense parts stay finer so they don't clot.
RADIUS = {"case-base": 1.3, "case-top": 1.3, "lilygo": 0.8, "sensor": 0.9}
# Edges sharper than this (degrees between faces) are drawn; higher shows more.
CREASE = {"case-base": 120, "case-top": 120, "lilygo": 100, "sensor": 110}

scene = bpy.context.scene
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.resolution_percentage = 100
cam = place_camera(scene, ortho_scale=ORTHO)
bpy.context.view_layer.update()  # matrix_world is stale until the depsgraph runs

parts = {name: bpy.data.objects[name] for name in OFFSETS}
for name, o in parts.items():
    o.location += OFFSETS[name]

# Travel in SVG pixels: ortho_scale spans the frame's width.
right = cam.matrix_world.to_3x3().col[0]
up = cam.matrix_world.to_3x3().col[1]
px = W / ORTHO
def to_svg(v):
    return [round(v.dot(right) * px, 1), round(-v.dot(up) * px, 1)]
travel = {name: to_svg(OFFSETS[name]) for name in parts}
waypoints = {name: [to_svg(w) for w in ws] for name, ws in WAYPOINTS.items()}

ink = bpy.data.materials.new("ink")
bpy.data.materials.create_gpencil_data(ink)
ink.grease_pencil.color = (0, 0, 0, 1)

for name, part in parts.items():
    for o in parts.values():
        o.lineart.usage = "INHERIT" if o is part else "EXCLUDE"
    gp = bpy.data.grease_pencils.new(name + "-lines")
    layer = gp.layers.new("lines")
    layer.frames.new(scene.frame_current)
    gp.materials.append(ink)
    obj = bpy.data.objects.new(name + "-lines", gp)
    scene.collection.objects.link(obj)
    mod = obj.modifiers.new("lineart", "LINEART")
    mod.source_type = "OBJECT"
    mod.source_object = part
    mod.target_layer = "lines"
    mod.target_material = ink
    mod.crease_threshold = math.radians(CREASE[name])
    mod.use_intersection = False
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Project the strokes ourselves: headless, the SVG exporter has no viewport
    # and picks its own projection.
    def to_px(co):
        v = world_to_camera_view(scene, cam, obj.matrix_world @ co)
        return [round(v.x * W, 2), round((1 - v.y) * H, 2)]
    drawing = gp.layers["lines"].frames[0].drawing
    lines = [[to_px(p.position) for p in stroke.points] for stroke in drawing.strokes]
    with open(os.path.join(out_dir, name + ".json"), "w") as f:
        json.dump({"width": RADIUS[name], "lines": lines}, f)
    print("LINES", name, len(lines), sum(map(len, lines)))
    obj.hide_render = True

# Silhouette masks: each part alone, flat white on black.
scene.render.engine = "BLENDER_WORKBENCH"
shading = scene.display.shading
shading.light, shading.color_type, shading.single_color = "FLAT", "SINGLE", (1, 1, 1)
shading.show_cavity = shading.show_shadows = shading.show_object_outline = False
scene.display.render_aa = "OFF"
scene.view_settings.view_transform = "Standard"
scene.render.film_transparent = False
world = bpy.data.worlds.new("black")
world.color = (0, 0, 0)
scene.world = world
for name, part in parts.items():
    for o in parts.values():
        o.hide_render = o is not part
    scene.render.filepath = os.path.join(out_dir, name + ".png")
    bpy.ops.render.render(write_still=True)

# The base's open top, projected: compose_lineart.py redraws the base's walls over
# the board and sensor everywhere but here, so they sink behind the walls but
# stay visible through the opening.
base = parts["case-base"]
lo = [min(v.co[i] for v in base.data.vertices) for i in range(3)]
hi = [max(v.co[i] for v in base.data.vertices) for i in range(3)]
opening = []
for x, y in ((lo[0], lo[1]), (hi[0], lo[1]), (hi[0], hi[1]), (lo[0], hi[1])):
    v = world_to_camera_view(scene, cam, base.matrix_world @ Vector((x, y, hi[2])))
    opening.append([round(v.x * W, 1), round((1 - v.y) * H, 1)])

with open(os.path.join(out_dir, "parts.json"), "w") as f:
    json.dump({"width": W, "height": H, "travel": travel, "waypoints": waypoints,
               "opening": opening}, f, indent=2)
print("TRAVEL", travel)
