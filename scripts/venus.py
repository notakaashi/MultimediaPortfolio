# Venus Python Script for Blender
import bpy

# Planet parameters
name = "Venus"
radius = 0.95
distance = 10.82
rotation_speed = 0.005

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
