import bpy
import math

# ==========================================
# CONFIG
# ==========================================
PLANET_NAME = "Uranus"
RING_NAME = "Uranus_Rings"
SPIN_FRAMES = 240
FPS = 24

RING_INNER = 18.0
RING_OUTER = 26.0
RING_THICKNESS = 0.1
RING_TILT = math.radians(82)  # Uranus rings are nearly vertical

# ==========================================
# SET UP SCENE
# ==========================================
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = SPIN_FRAMES

# Remove existing ring if present
if RING_NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[RING_NAME], do_unlink=True)

# ==========================================
# GET URANUS
# ==========================================
if PLANET_NAME not in bpy.data.objects:
    print(f"❌ Object '{PLANET_NAME}' not found!")
else:
    uranus = bpy.data.objects[PLANET_NAME]
    
    # ==========================================
    # CREATE RINGS (TORUS)
    # ==========================================
    bpy.ops.mesh.primitive_torus_add(
        major_radius=(RING_INNER + RING_OUTER) / 2,
        minor_radius=(RING_OUTER - RING_INNER) / 2,
        location=(0, 0, 0)
    )
    rings = bpy.context.active_object
    rings.name = RING_NAME
    rings.scale.z = RING_THICKNESS
    rings.rotation_euler = (RING_TILT, 0, 0)
    
    # ==========================================
    # RING MATERIAL
    # ==========================================
    ring_mat = bpy.data.materials.new(name="UranusRingMaterial")
    ring_mat.use_nodes = True
    nodes = ring_mat.node_tree.nodes
    links = ring_mat.node_tree.links
    
    for n in nodes:
        nodes.remove(n)
    
    r_out = nodes.new("ShaderNodeOutputMaterial")
    r_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    r_tex = nodes.new("ShaderNodeTexNoise")
    r_ramp = nodes.new("ShaderNodeValToRGB")
    r_coord = nodes.new("ShaderNodeTexCoord")
    r_map = nodes.new("ShaderNodeMapping")
    
    r_coord.location = (-800, 0)
    r_map.location = (-600, 0)
    r_tex.location = (-400, 0)
    r_ramp.location = (-200, 0)
    r_bsdf.location = (0, 0)
    r_out.location = (200, 0)
    
    r_map.inputs["Scale"].default_value = (20.0, 1.0, 1.0)
    r_tex.inputs["Scale"].default_value = 12.0
    r_tex.inputs["Detail"].default_value = 2.0
    
    r_ramp.color_ramp.elements[0].position = 0.3
    r_ramp.color_ramp.elements[1].position = 0.7
    r_ramp.color_ramp.elements[0].color = (0.3, 0.3, 0.35, 1)
    r_ramp.color_ramp.elements[1].color = (0.5, 0.5, 0.55, 1)
    
    links.new(r_coord.outputs["Object"], r_map.inputs["Vector"])
    links.new(r_map.outputs["Vector"], r_tex.inputs["Vector"])
    links.new(r_tex.outputs["Fac"], r_ramp.inputs["Fac"])
    links.new(r_ramp.outputs["Color"], r_bsdf.inputs["Base Color"])
    links.new(r_bsdf.outputs["BSDF"], r_out.inputs["Surface"])
    
    if rings.data.materials:
        rings.data.materials[0] = ring_mat
    else:
        rings.data.materials.append(ring_mat)
    
    # Parent rings to Uranus
    rings.parent = uranus
    
    # ==========================================
    # ANIMATE RINGS WITH URANUS
    # ==========================================
    rings.rotation_mode = 'XYZ'
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    
    scene.frame_set(1)
    rings.rotation_euler = (RING_TILT, 0, 0)
    rings.keyframe_insert(data_path="rotation_euler", frame=1)
    
    scene.frame_set(SPIN_FRAMES)
    rings.rotation_euler = (RING_TILT, 0, math.radians(360))
    rings.keyframe_insert(data_path="rotation_euler", frame=SPIN_FRAMES)
    
    scene.frame_set(1)
    print("✅ Uranus rings created and animated!")