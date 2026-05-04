# Jupiter Python Script for Blender
import bpy

# Planet parameters
name = "Jupiter"
radius = 11.2
distance = 77.83
rotation_speed = 0.02

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
