# Sun Python Script for Blender
import bpy

# Add Sun light
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0))
