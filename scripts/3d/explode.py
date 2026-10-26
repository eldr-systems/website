# The burst both renders share: how far each part of keep.blend travels from its
# assembled position, in mm, and the camera that watches it. render_video.py
# animates between the two poses; render_lineart.py draws the exploded pose.
import math
from mathutils import Vector

OFFSETS = {
    "case-top": Vector((0, 0, 92)),     # lid lifts straight off
    "lilygo":   Vector((0, 0, 48)),     # board rises out of the base
    "sensor":   Vector((0, 0, 62)),     # drops out of the lid's pocket, hangs between
    "case-base": Vector((0, 0, 0)),
}

# Stops on the way, so a part clears the walls instead of passing through them.
# None needed now: the sensor sits in the lid and every part moves straight up.
WAYPOINTS = {}

# Seen from the front-right, a little above: the lid, board and sensor all read.
CAMERA_TARGET = Vector((-8, 0, 80))
CAMERA_DIRECTION = Vector((0.85, -1.0, 0.62)).normalized()
CAMERA_DISTANCE = 760
CAMERA_LENS = 70  # mm; long enough that the box doesn't distort

def place_camera(scene, ortho_scale=None):
    import bpy
    cam = scene.camera
    if cam is None:
        cam = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
        scene.collection.objects.link(cam)
        scene.camera = cam
    cam.location = CAMERA_TARGET + CAMERA_DIRECTION * CAMERA_DISTANCE
    cam.rotation_euler = (-CAMERA_DIRECTION).to_track_quat("-Z", "Y").to_euler()
    cam.data.clip_end = 5000
    if ortho_scale:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
    else:
        cam.data.lens = CAMERA_LENS
    return cam
