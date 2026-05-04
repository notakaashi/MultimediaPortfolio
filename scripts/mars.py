import bpy
import math

# ==========================================
# 1. CLEAN UP THE SCENE
# ==========================================
# Delete all mesh objects
for obj in list(bpy.data.objects):
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)

# Delete all lights
for obj in list(bpy.data.objects):
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# ==========================================
# 2. CREATE THE MARS OBJECT
# ==========================================
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=128, 
    ring_count=64, 
    radius=6.5, 
    location=(0, 0, 0)
)
mars = bpy.context.active_object
mars.name = "Mars_Model"
bpy.ops.object.shade_smooth()

# ==========================================
# 3. ADD LIGHTING
# ==========================================

# Main Sun Light
bpy.ops.object.light_add(
    type='SUN',
    location=(30, 20, 20)
)
sun_light = bpy.context.active_object
sun_light.name = "Sun_Light"
sun_light.data.energy = 3.0
sun_light.data.color = (1.0, 1.0, 0.95)

# Fill Light
bpy.ops.object.light_add(
    type='SUN',
    location=(-20, -10, -15)
)
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 1.0
fill_light.data.color = (0.6, 0.7, 1.0)

# ==========================================
# 4. ANIMATE THE ROTATION
# ==========================================
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250
mars.rotation_mode = 'XYZ'

original_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# Insert keyframes
bpy.context.scene.frame_set(1)
mars.rotation_euler = (0, 0, 0)
mars.keyframe_insert(data_path="rotation_euler", index=2, frame=1)

bpy.context.scene.frame_set(250)
mars.rotation_euler = (0, 0, math.radians(360))
mars.keyframe_insert(data_path="rotation_euler", index=2, frame=250)

bpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp
bpy.context.scene.frame_set(1)

print("✅ Mars created with lighting!")