import bpy
import math

# ---------------------------------------------------------
# 1. CLEANUP: Remove old Pluto and Sun if we run this twice
# ---------------------------------------------------------
for obj_name in ["Pluto", "Pluto_Sun"]:
    if obj_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

# ---------------------------------------------------------
# 2. CREATE THE PLANET MESH
# ---------------------------------------------------------
# Create a high-res sphere so the shadows look smooth
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=1, location=(0, 0, 0))
pluto = bpy.context.active_object
pluto.name = "Pluto"
bpy.ops.object.shade_smooth() # Make it smooth!

# ---------------------------------------------------------
# 3. CREATE THE PROCEDURAL TEXTURE (No images needed!)
# ---------------------------------------------------------
mat_name = "Pluto_Surface"
if mat_name in bpy.data.materials:
    bpy.data.materials.remove(bpy.data.materials[mat_name])

mat = bpy.data.materials.new(name=mat_name)
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create standard output and Principled BSDF
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)
principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.location = (100, 0)
principled.inputs['Roughness'].default_value = 0.75 # Rocky and dry

# Create Noise Texture to generate the rocky/icy patterns
noise = nodes.new(type='ShaderNodeTexNoise')
noise.location = (-500, 0)
noise.inputs['Scale'].default_value = 2.5
noise.inputs['Detail'].default_value = 15.0
noise.inputs['Roughness'].default_value = 0.65

# Create ColorRamp to assign Pluto's actual colors to the noise
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (-200, 0)
color_ramp.color_ramp.elements[0].position = 0.35
color_ramp.color_ramp.elements[0].color = (0.15, 0.08, 0.06, 1.0) # Dark reddish brown
color_ramp.color_ramp.elements[1].position = 0.55
color_ramp.color_ramp.elements[1].color = (0.5, 0.35, 0.25, 1.0)  # Dusty tan
# Add a third color stop for the icy pale patches
color_ramp.color_ramp.elements.new(0.7)
color_ramp.color_ramp.elements[2].color = (0.8, 0.75, 0.7, 1.0)   # Pale ice

# Create Bump Map to fake 3D craters using the noise data
bump = nodes.new(type='ShaderNodeBump')
bump.location = (-200, -300)
bump.inputs['Strength'].default_value = 0.15 # Keep it subtle so shadows don't break
bump.inputs['Distance'].default_value = 0.2

# Link the material nodes together
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(bump.outputs['Normal'], principled.inputs['Normal'])
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Assign the material to the Pluto sphere
if pluto.data.materials:
    pluto.data.materials[0] = mat
else:
    pluto.data.materials.append(mat)

# ---------------------------------------------------------
# 4. ADD LIGHTING
# ---------------------------------------------------------
# Create a harsh, distant sun to match deep space
light_data = bpy.data.lights.new(name="Pluto_Sun_Light", type='SUN')
light_data.energy = 3.0
light_data.angle = math.radians(2.0) # Slightly soft shadows to avoid terminator noise!

light_obj = bpy.data.objects.new(name="Pluto_Sun", object_data=light_data)
bpy.context.collection.objects.link(light_obj)
light_obj.location = (5, -5, 2)
# Angle the sun at the planet
light_obj.rotation_euler = (math.radians(60), 0, math.radians(45)) 

# ---------------------------------------------------------
# 5. ANIMATE THE ROTATION
# ---------------------------------------------------------
pluto.rotation_mode = 'XYZ'
start_frame = 1
end_frame = 250

user_pref_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

pluto.rotation_euler[2] = 0
pluto.keyframe_insert(data_path="rotation_euler", index=2, frame=start_frame)

pluto.rotation_euler[2] = math.radians(360)
pluto.keyframe_insert(data_path="rotation_euler", index=2, frame=end_frame)

bpy.context.preferences.edit.keyframe_new_interpolation_type = user_pref_interp

print("Success: Procedural Pluto with Textures, Lighting, and Animation generated!")