import bpy
import math

# ==========================================
# 1. CLEAN UP THE SCENE
# ==========================================
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
bpy.ops.object.delete()

# Delete existing lights
for obj in bpy.context.scene.objects:
    if obj.type == 'LIGHT':
        obj.select_set(True)
bpy.ops.object.delete()

# ==========================================
# 2. CREATE THE VENUS OBJECT
# ==========================================
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=128, 
    ring_count=64, 
    radius=8.0, 
    location=(0, 0, 0)
)
venus = bpy.context.active_object
venus.name = "Venus_Model"
bpy.ops.object.shade_smooth()

# ==========================================
# 3. ADD LIGHTING
# ==========================================

# Main Sun Light (bright yellow, front-left)
bpy.ops.object.light_add(
    type='SUN',
    location=(30, 20, 20)
)
sun_light = bpy.context.active_object
sun_light.name = "Sun_Light"
sun_light.data.energy = 3.0
sun_light.data.color = (1.0, 0.95, 0.8)  # Warm yellow

# Fill Light (softer, from back)
bpy.ops.object.light_add(
    type='SUN',
    location=(-20, -10, -15)
)
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 1.0
fill_light.data.color = (0.6, 0.7, 1.0)  # Cool blue

# ==========================================
# 4. ANIMATE THE ROTATION
# ==========================================
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250
venus.rotation_mode = 'XYZ'

original_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# Insert keyframes
bpy.context.scene.frame_set(1)
venus.rotation_euler = (0, 0, 0)
venus.keyframe_insert(data_path="rotation_euler", index=2, frame=1)

bpy.context.scene.frame_set(250)
venus.rotation_euler = (0, 0, math.radians(360))
venus.keyframe_insert(data_path="rotation_euler", index=2, frame=250)

bpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp
bpy.context.scene.frame_set(1)

print("✅ Venus created with lighting!")