# Neptune Python Script for Blender
import bpy

# Planet parameters
name = "Neptune"
radius = 3.88
distance = 449.7
rotation_speed = 0.012

# Create sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))
obj = bpy.context.active_object
obj.name = name
