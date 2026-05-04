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

# ==========================================
# 2. CREATE THE MERCURY OBJECT
# ==========================================
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=128, 
    ring_count=64, 
    radius=5.0, 
    location=(0, 0, 0)
)
mercury = bpy.context.active_object
mercury.name = "Mercury_Model"
bpy.ops.object.shade_smooth()

# ==========================================
# 3. ANIMATE THE ROTATION
# ==========================================
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250
mercury.rotation_mode = 'XYZ'

original_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# Insert keyframes
bpy.context.scene.frame_set(1)
mercury.rotation_euler = (0, 0, 0)
mercury.keyframe_insert(data_path="rotation_euler", index=2, frame=1)

bpy.context.scene.frame_set(250)
mercury.rotation_euler = (0, 0, math.radians(360))
mercury.keyframe_insert(data_path="rotation_euler", index=2, frame=250)

bpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp
bpy.context.scene.frame_set(1)

print("✅ Mercury created!")