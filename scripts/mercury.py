# Mercury Python Script for Blender
import bpy

# Planet parameters
name = "Mercury"
radius = 0.38
distance = 5.79
rotation_speed = 0.01

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
