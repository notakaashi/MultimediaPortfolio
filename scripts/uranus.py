# Uranus Python Script for Blender
import bpy

# Planet parameters
name = "Uranus"
radius = 4.0
distance = 287.1
rotation_speed = 0.015

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
