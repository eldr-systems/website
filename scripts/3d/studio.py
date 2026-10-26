# The look every video of The Keep shares: brand colours, a bone floor that fills
# the frame, three lights, and render settings that keep the colours exact.
# shaded() is the studio render; lineart() swaps it for an ink-on-bone drawing.
import math
import bpy
from mathutils import Vector

BONE, RULE, INK = "#F4F1EA", "#C9C3B6", "#14161A"

def srgb(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

def output(scene, out_dir, frame_start, frame_end, fps=30):
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = 1440, 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = frame_start, frame_end
    scene.view_settings.view_transform = "Standard"  # keep brand colours exact
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = out_dir.rstrip("/") + "/f"

def ground(scene):
    bpy.ops.mesh.primitive_plane_add(size=4000)
    plane = bpy.context.object
    plane.name = "ground"
    m = bpy.data.materials.new("ground")
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb(BONE)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    plane.data.materials.append(m)
    return plane

def shaded(scene):
    """Studio render: soft light, contact shadows on a bone floor."""
    # The case in the site's rule tone: bone-on-bone would vanish against the page.
    bpy.data.materials["case"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb(RULE)
    ground(scene)
    world = bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = srgb(BONE)
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

    light("key", "SUN", 3.2, (-200, -260, 420), 8)
    light("fill", "AREA", 1.6e6, (420, -160, 200), 300)
    light("rim", "AREA", 1.0e6, (-120, 400, 260), 250)
    scene.view_settings.exposure = -0.7

def lineart(scene, parts, radius=0.22, crease=120):
    """Technical drawing: every surface flat bone, ink Line Art over the parts,
    with true occlusion between them. radius is the line's half-width in mm."""
    flat = bpy.data.materials.new("flat-bone")
    flat.use_nodes = True
    nodes = flat.node_tree.nodes
    nodes.clear()
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = srgb(BONE)
    out = nodes.new("ShaderNodeOutputMaterial")
    flat.node_tree.links.new(emit.outputs[0], out.inputs[0])
    for o in parts:
        o.data.materials.clear()
        o.data.materials.append(flat)
    plane = ground(scene)
    plane.data.materials.clear()
    plane.data.materials.append(flat)
    plane.lineart.usage = "EXCLUDE"

    world = bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = srgb(BONE)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1

    coll = bpy.data.collections.new("drawn")
    scene.collection.children.link(coll)
    for o in parts:
        coll.objects.link(o)
    ink = bpy.data.materials.new("ink")
    bpy.data.materials.create_gpencil_data(ink)
    ink.grease_pencil.color = srgb(INK)
    gp = bpy.data.grease_pencils.new("lines")
    gp.layers.new("lines").frames.new(scene.frame_start)
    gp.materials.append(ink)
    obj = bpy.data.objects.new("lines", gp)
    scene.collection.objects.link(obj)
    mod = obj.modifiers.new("lineart", "LINEART")
    mod.source_type = "COLLECTION"
    mod.source_collection = coll
    mod.target_layer = "lines"
    mod.target_material = ink
    mod.radius = radius
    mod.crease_threshold = math.radians(crease)
    mod.use_intersection = False
    scene.view_settings.exposure = 0
    return obj
