# Earth Python Script for Blender
import bpy

# Planet parameters
name = "Earth"
radius = 1.0
distance = 14.96
rotation_speed = 0.01

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
