import bpy
import math

# ==========================================
# CONFIG
# ==========================================
PLANET_NAME = "Neptune"
SPIN_FRAMES = 240
FPS = 24

# ==========================================
# SET UP SCENE
# ==========================================
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = SPIN_FRAMES

# Remove existing objects if present
if PLANET_NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[PLANET_NAME], do_unlink=True)

# Remove all lights
for obj in list(bpy.data.objects):
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# ==========================================
# CREATE NEPTUNE
# ==========================================
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=128,
    ring_count=64,
    radius=14.5,
    location=(0, 0, 0)
)
neptune = bpy.context.active_object
neptune.name = PLANET_NAME
bpy.ops.object.shade_smooth()

# ==========================================
# ADD LIGHTING
# ==========================================

# Main Sun Light
bpy.ops.object.light_add(
    type='SUN',
    location=(30, 20, 20)
)
sun_light = bpy.context.active_object
sun_light.name = "Neptune_KeyLight"
sun_light.data.energy = 3.0
sun_light.data.color = (1.0, 1.0, 0.95)

# Fill Light
bpy.ops.object.light_add(
    type='SUN',
    location=(-20, -10, -15)
)
fill_light = bpy.context.active_object
fill_light.name = "Neptune_FillLight"
fill_light.data.energy = 1.0
fill_light.data.color = (0.6, 0.7, 1.0)

# ==========================================
# ANIMATE SPIN - Left to right
# ==========================================
neptune.rotation_mode = 'XYZ'
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# Neptune rotation - rotates around Z axis (left to right)
scene.frame_set(1)
neptune.rotation_euler = (0, 0, 0)
neptune.keyframe_insert(data_path="rotation_euler", frame=1)

scene.frame_set(SPIN_FRAMES)
neptune.rotation_euler = (0, 0, math.radians(360))
neptune.keyframe_insert(data_path="rotation_euler", frame=SPIN_FRAMES)

scene.frame_set(1)

print("✅ Neptune created with left to right spin!")