# Mars Python Script for Blender
import bpy

# Planet parameters
name = "Mars"
radius = 0.53
distance = 22.79
rotation_speed = 0.008

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
