import bpy
import math

# ==========================================
# 1. THE SPIN (Targeting "The Sun")
# ==========================================
sun_name = "The Sun"
sun = bpy.data.objects.get(sun_name)

if sun is not None:
    sun.animation_data_clear() # Reset previous animation
    
    # Frame 1: 0 degrees
    sun.rotation_euler[2] = 0  
    sun.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    
    # Frame 250: 360 degrees
    sun.rotation_euler[2] = math.radians(360)
    sun.keyframe_insert(data_path="rotation_euler", index=2, frame=250)
    
    # Make rotation linear and infinite
    if sun.animation_data and sun.animation_data.action:
        action = sun.animation_data.action
        
        # --- BLENDER 5.0+ COMPATIBILITY FIX ---
        if hasattr(action, "fcurves"):
            fcurves = action.fcurves
        else:
            from bpy_extras import anim_utils
            bag = anim_utils.action_get_channelbag_for_slot(action, sun.animation_data.action_slot)
            fcurves = bag.fcurves if bag else []
            
        for fcurve in fcurves:
            if fcurve.data_path == 'rotation_euler':
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'LINEAR'
                mod = fcurve.modifiers.new(type='CYCLES')
                mod.mode_before = 'REPEAT'
                mod.mode_after = 'REPEAT'
                
    print(f"Spin applied to '{sun_name}'.")
else:
    print(f"Error: Could not find '{sun_name}'.")

# ==========================================
# 2. THE FLARE (Targeting "Flare")
# ==========================================
flare_name = "Flare"
flare = bpy.data.objects.get(flare_name)

if flare is not None:
    flare.animation_data_clear() # Reset previous animation
    
    # Frame 1: Hidden / Flat against the surface
    flare.scale = (0.1, 0.1, 0.1) 
    flare.keyframe_insert(data_path="scale", frame=1)

    # Frame 60: Eruption (Shoots outward)
    flare.scale = (1.5, 1.5, 1.5) 
    flare.keyframe_insert(data_path="scale", frame=60)

    # Frame 120: Retracts back into the sun
    flare.scale = (0.1, 0.1, 0.1)
    flare.keyframe_insert(data_path="scale", frame=120)

    # Make the eruption cycle infinitely
    if flare.animation_data and flare.animation_data.action:
        action = flare.animation_data.action
        
        # --- BLENDER 5.0+ COMPATIBILITY FIX ---
        if hasattr(action, "fcurves"):
            fcurves = action.fcurves
        else:
            from bpy_extras import anim_utils
            bag = anim_utils.action_get_channelbag_for_slot(action, flare.animation_data.action_slot)
            fcurves = bag.fcurves if bag else []

        for fcurve in fcurves:
            if fcurve.data_path == 'scale':
                mod = fcurve.modifiers.new(type='CYCLES')
                mod.mode_before = 'REPEAT'
                mod.mode_after = 'REPEAT'
                
    print(f"Eruption applied to '{flare_name}'.")
else:
    print(f"Error: Could not find '{flare_name}'.")

print("All animations applied! Press Spacebar to play.") 