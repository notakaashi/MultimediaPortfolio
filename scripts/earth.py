import bpy
import math
import os

# ==========================================
# 1. CLEAN UP THE SCENE
# ==========================================
# Delete all mesh objects
for obj in list(bpy.data.objects):
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)

# Delete all lights
for obj in list(bpy.data.objects):
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# ==========================================
# 2. CREATE THE EARTH OBJECT
# ==========================================
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=128, 
    ring_count=64, 
    radius=12.0, 
    location=(0, 0, 0)
)
earth = bpy.context.active_object
earth.name = "Earth_Model"
bpy.ops.object.shade_smooth()

# ==========================================
# 3. CREATE MATERIAL WITH YOUR IMAGE
# ==========================================
mat = bpy.data.materials.new(name="Earth_Mat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

nodes.clear()

# Output Node
out_node = nodes.new('ShaderNodeOutputMaterial')
out_node.location = (400, 0)

# Principled BSDF
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (100, 0)
bsdf.inputs['Roughness'].default_value = 0.5

# Image Texture Node
tex_color = nodes.new('ShaderNodeTexImage')
tex_color.location = (-300, 0)

# Load your Earth image
image_path = r"C:\Users\Admin\Downloads\earth.jpg"
if os.path.exists(image_path):
    image = bpy.data.images.load(image_path)
    tex_color.image = image
    print(f"✅ Earth texture loaded: {image_path}")
else:
    print(f"❌ Image not found: {image_path}")

# Connect nodes
links.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

# Assign Material
if len(earth.data.materials) == 0:
    earth.data.materials.append(mat)
else:
    earth.data.materials[0] = mat

# ==========================================
# 4. ADD LIGHTING
# ==========================================

# Main Sun Light
bpy.ops.object.light_add(
    type='SUN',
    location=(30, 20, 20)
)
sun_light = bpy.context.active_object
sun_light.name = "Sun_Light"
sun_light.data.energy = 3.0
sun_light.data.color = (1.0, 1.0, 0.95)

# Fill Light
bpy.ops.object.light_add(
    type='SUN',
    location=(-20, -10, -15)
)
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 1.0
fill_light.data.color = (0.6, 0.7, 1.0)

# ==========================================
# 5. ANIMATE THE ROTATION
# ==========================================
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250
earth.rotation_mode = 'XYZ'

original_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# Insert keyframes
bpy.context.scene.frame_set(1)
earth.rotation_euler = (0, 0, 0)
earth.keyframe_insert(data_path="rotation_euler", index=2, frame=1)

bpy.context.scene.frame_set(250)
earth.rotation_euler = (0, 0, math.radians(360))
earth.keyframe_insert(data_path="rotation_euler", index=2, frame=250)

bpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp
bpy.context.scene.frame_set(1)

print("✅ Earth created with your image texture!")