import bpy
import math

# ==========================================
# CONFIG
# ==========================================
PLANET_NAME = "Saturn"
SPIN_FRAMES = 240
FPS = 24

# ==========================================
# SET UP SCENE
# ==========================================
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = SPIN_FRAMES

# ==========================================
# GET SATURN MODEL
# ==========================================
if PLANET_NAME not in bpy.data.objects:
    print(f"❌ Object '{PLANET_NAME}' not found!")
else:
    saturn = bpy.data.objects[PLANET_NAME]
    saturn.rotation_mode = 'XYZ'
    
    # ==========================================
    # ANIMATE SPIN
    # ==========================================
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    
    scene.frame_set(1)
    saturn.rotation_euler = (0, 0, 0)
    saturn.keyframe_insert(data_path="rotation_euler", frame=1)
    
    scene.frame_set(SPIN_FRAMES)
    saturn.rotation_euler = (0, 0, math.radians(360))
    saturn.keyframe_insert(data_path="rotation_euler", frame=SPIN_FRAMES)
    
    scene.frame_set(1)
    print("✅ Saturn animation created!")