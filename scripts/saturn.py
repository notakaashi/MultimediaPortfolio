# Saturn Python Script for Blender
import bpy

# Planet parameters
name = "Saturn"
radius = 9.45
distance = 142.7
rotation_speed = 0.018

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
