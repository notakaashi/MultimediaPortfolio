/* jshint esversion: 6 */
/**
 * solarsystem.js - Interactive logic for Solar System page
 */

const scripts = {
    sun: `import bpy
import math

# ==========================================
# 1. THE SPIN (Targeting "The Sun")
# ==========================================
sun_name = "The Sun"
sun = bpy.data.objects.get(sun_name)

if sun is not None:
    sun.animation_data_clear() # Reset previous animation
    
    # Frame 1: 0 degrees
    sun.rotation_euler[2] = 0  
    sun.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    
    # Frame 250: 360 degrees
    sun.rotation_euler[2] = math.radians(360)
    sun.keyframe_insert(data_path="rotation_euler", index=2, frame=250)
    
    # Make rotation linear and infinite
    if sun.animation_data and sun.animation_data.action:
        action = sun.animation_data.action
        
        # --- BLENDER 5.0+ COMPATIBILITY FIX ---
        if hasattr(action, "fcurves"):
            fcurves = action.fcurves
        else:
            from bpy_extras import anim_utils
            bag = anim_utils.action_get_channelbag_for_slot(action, sun.animation_data.action_slot)
            fcurves = bag.fcurves if bag else []
            
        for fcurve in fcurves:
            if fcurve.data_path == 'rotation_euler':
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'LINEAR'
                mod = fcurve.modifiers.new(type='CYCLES')
                mod.mode_before = 'REPEAT'
                mod.mode_after = 'REPEAT'
                
    print(f"Spin applied to '{sun_name}'.")
else:
    print(f"Error: Could not find '{sun_name}'.")

# ==========================================
# 2. THE FLARE (Targeting "Flare")
# ==========================================
flare_name = "Flare"
flare = bpy.data.objects.get(flare_name)

if flare is not None:
    flare.animation_data_clear() # Reset previous animation
    
    # Frame 1: Hidden / Flat against the surface
    flare.scale = (0.1, 0.1, 0.1) 
    flare.keyframe_insert(data_path="scale", frame=1)

    # Frame 60: Eruption (Shoots outward)
    flare.scale = (1.5, 1.5, 1.5) 
    flare.keyframe_insert(data_path="scale", frame=60)

    # Frame 120: Retracts back into the sun
    flare.scale = (0.1, 0.1, 0.1)
    flare.keyframe_insert(data_path="scale", frame=120)

    # Make the eruption cycle infinitely
    if flare.animation_data and flare.animation_data.action:
        action = flare.animation_data.action
        
        # --- BLENDER 5.0+ COMPATIBILITY FIX ---
        if hasattr(action, "fcurves"):
            fcurves = action.fcurves
        else:
            from bpy_extras import anim_utils
            bag = anim_utils.action_get_channelbag_for_slot(action, flare.animation_data.action_slot)
            fcurves = bag.fcurves if bag else []

        for fcurve in fcurves:
            if fcurve.data_path == 'scale':
                mod = fcurve.modifiers.new(type='CYCLES')
                mod.mode_before = 'REPEAT'
                mod.mode_after = 'REPEAT'
                
    print(f"Eruption applied to '{flare_name}'.")
else:
    print(f"Error: Could not find '{flare_name}'.")

print("All animations applied! Press Spacebar to play.")`,
    mercury: `import bpy\nimport math\n\n# ==========================================\n# 1. CLEAN UP THE SCENE\n# ==========================================\nbpy.ops.object.select_all(action='DESELECT')\nfor obj in bpy.context.scene.objects:\n    if obj.type == 'MESH':\n        obj.select_set(True)\nbpy.ops.object.delete()\n\n# ==========================================\n# 2. CREATE THE MERCURY OBJECT\n# ==========================================\nbpy.ops.mesh.primitive_uv_sphere_add(\n    segments=128, \n    ring_count=64, \n    radius=5.0, \n    location=(0, 0, 0)\n)\nmercury = bpy.context.active_object\nmercury.name = "Mercury_Model"\nbpy.ops.object.shade_smooth()\n\n# ==========================================\n# 3. ANIMATE THE ROTATION\n# ==========================================\nbpy.context.scene.frame_start = 1\nbpy.context.scene.frame_end = 250\nmercury.rotation_mode = 'XYZ'\n\noriginal_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type\nbpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n\n# Insert keyframes\nbpy.context.scene.frame_set(1)\nmercury.rotation_euler = (0, 0, 0)\nmercury.keyframe_insert(data_path="rotation_euler", index=2, frame=1)\n\nbpy.context.scene.frame_set(250)\nmercury.rotation_euler = (0, 0, math.radians(360))\nmercury.keyframe_insert(data_path="rotation_euler", index=2, frame=250)\n\nbpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp\nbpy.context.scene.frame_set(1)\n\nprint("✅ Mercury created!")`,
    venus: `import bpy\nimport math\n\n# ==========================================\n# 1. CLEAN UP THE SCENE\n# ==========================================\nbpy.ops.object.select_all(action='DESELECT')\nfor obj in bpy.context.scene.objects:\n    if obj.type == 'MESH':\n        obj.select_set(True)\nbpy.ops.object.delete()\n\n# Delete existing lights\nfor obj in bpy.context.scene.objects:\n    if obj.type == 'LIGHT':\n        obj.select_set(True)\nbpy.ops.object.delete()\n\n# ==========================================\n# 2. CREATE THE VENUS OBJECT\n# ==========================================\nbpy.ops.mesh.primitive_uv_sphere_add(\n    segments=128, \n    ring_count=64, \n    radius=8.0, \n    location=(0, 0, 0)\n)\nvenus = bpy.context.active_object\nvenus.name = "Venus_Model"\nbpy.ops.object.shade_smooth()\n\n# ==========================================\n# 3. ADD LIGHTING\n# ==========================================\n\n# Main Sun Light (bright yellow, front-left)\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(30, 20, 20)\n)\nsun_light = bpy.context.active_object\nsun_light.name = "Sun_Light"\nsun_light.data.energy = 3.0\nsun_light.data.color = (1.0, 0.95, 0.8)  # Warm yellow\n\n# Fill Light (softer, from back)\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(-20, -10, -15)\n)\nfill_light = bpy.context.active_object\nfill_light.name = "Fill_Light"\nfill_light.data.energy = 1.0\nfill_light.data.color = (0.6, 0.7, 1.0)  # Cool blue\n\n# ==========================================\n# 4. ANIMATE THE ROTATION\n# ==========================================\nbpy.context.scene.frame_start = 1\nbpy.context.scene.frame_end = 250\nvenus.rotation_mode = 'XYZ'\n\noriginal_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type\nbpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n\n# Insert keyframes\nbpy.context.scene.frame_set(1)\nvenus.rotation_euler = (0, 0, 0)\nvenus.keyframe_insert(data_path="rotation_euler", index=2, frame=1)\n\nbpy.context.scene.frame_set(250)\nvenus.rotation_euler = (0, 0, math.radians(360))\nvenus.keyframe_insert(data_path="rotation_euler", index=2, frame=250)\n\nbpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp\nbpy.context.scene.frame_set(1)\n\nprint("✅ Venus created!")`,
    earth: `import bpy\nimport math\nimport os\n\n# ==========================================\n# 1. CLEAN UP THE SCENE\n# ==========================================\n# Delete all mesh objects\nfor obj in list(bpy.data.objects):\n    if obj.type == 'MESH':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# Delete all lights\nfor obj in list(bpy.data.objects):\n    if obj.type == 'LIGHT':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# ==========================================\n# 2. CREATE THE EARTH OBJECT\n# ==========================================\nbpy.ops.mesh.primitive_uv_sphere_add(\n    segments=128, \n    ring_count=64, \n    radius=12.0, \n    location=(0, 0, 0)\n)\nearth = bpy.context.active_object\nearth.name = "Earth_Model"\nbpy.ops.object.shade_smooth()\n\n# ==========================================\n# 3. CREATE MATERIAL WITH YOUR IMAGE\n# ==========================================\nmat = bpy.data.materials.new(name="Earth_Mat")\nmat.use_nodes = True\nnodes = mat.node_tree.nodes\nlinks = mat.node_tree.links\n\nnodes.clear()\n\n# Output Node\nout_node = nodes.new('ShaderNodeOutputMaterial')\nout_node.location = (400, 0)\n\n# Principled BSDF\nbsdf = nodes.new('ShaderNodeBsdfPrincipled')\nbsdf.location = (100, 0)\nbsdf.inputs['Roughness'].default_value = 0.5\n\n# Image Texture Node\ntex_color = nodes.new('ShaderNodeTexImage')\ntex_color.location = (-300, 0)\n\n# Load your Earth image\nimage_path = r"C:\\Users\\Admin\\Downloads\\earth.jpg"\nif os.path.exists(image_path):\n    image = bpy.data.images.load(image_path)\n    tex_color.image = image\n    print(f"✅ Earth texture loaded: {image_path}")\nelse:\n    print(f"❌ Image not found: {image_path}")\n\n# Connect nodes\nlinks.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])\nlinks.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])\n\n# Assign Material\nif len(earth.data.materials) == 0:\n    earth.data.materials.append(mat)\nelse:\n    earth.data.materials[0] = mat\n\n# ==========================================\n# 4. ANIMATE THE ROTATION\n# ==========================================\nbpy.context.scene.frame_start = 1\nbpy.context.scene.frame_end = 250\nearth.rotation_mode = 'XYZ'\n\noriginal_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type\nbpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n\n# Insert keyframes\nbpy.context.scene.frame_set(1)\nearth.rotation_euler = (0, 0, 0)\nearth.keyframe_insert(data_path="rotation_euler", index=2, frame=1)\n\nbpy.context.scene.frame_set(250)\nearth.rotation_euler = (0, 0, math.radians(360))\nearth.keyframe_insert(data_path="rotation_euler", index=2, frame=250)\n\nbpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp\nbpy.context.scene.frame_set(1)\n\nprint("✅ Earth created!")`,
    mars: `import bpy\nimport math\n\n# ==========================================\n# 1. CLEAN UP THE SCENE\n# ==========================================\n# Delete all mesh objects\nfor obj in list(bpy.data.objects):\n    if obj.type == 'MESH':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# Delete all lights\nfor obj in list(bpy.data.objects):\n    if obj.type == 'LIGHT':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# ==========================================\n# 2. CREATE THE MARS OBJECT\n# ==========================================\nbpy.ops.mesh.primitive_uv_sphere_add(\n    segments=128, \n    ring_count=64, \n    radius=6.5, \n    location=(0, 0, 0)\n)\nmars = bpy.context.active_object\nmars.name = "Mars_Model"\nbpy.ops.object.shade_smooth()\n\n# ==========================================\n# 3. ADD LIGHTING\n# ==========================================\n\n# Main Sun Light\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(30, 20, 20)\n)\nsun_light = bpy.context.active_object\nsun_light.name = "Sun_Light"\nsun_light.data.energy = 3.0\nsun_light.data.color = (1.0, 1.0, 0.95)\n\n# Fill Light\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(-20, -10, -15)\n)\nfill_light = bpy.context.active_object\nfill_light.name = "Fill_Light"\nfill_light.data.energy = 1.0\nfill_light.data.color = (0.6, 0.7, 1.0)\n\n# ==========================================\n# 4. ANIMATE THE ROTATION\n# ==========================================\nbpy.context.scene.frame_start = 1\nbpy.context.scene.frame_end = 250\nmars.rotation_mode = 'XYZ'\n\noriginal_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type\nbpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n\n# Insert keyframes\nbpy.context.scene.frame_set(1)\nmars.rotation_euler = (0, 0, 0)\nmars.keyframe_insert(data_path="rotation_euler", index=2, frame=1)\n\nbpy.context.scene.frame_set(250)\nmars.rotation_euler = (0, 0, math.radians(360))\nmars.keyframe_insert(data_path="rotation_euler", index=2, frame=250)\n\nbpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp\nbpy.context.scene.frame_set(1)\n\nprint("✅ Mars created!")`,
    jupiter: `import bpy\nimport math\n\n# ==========================================\n# 1. CLEAN UP THE SCENE\n# ==========================================\n# Delete all mesh objects\nfor obj in list(bpy.data.objects):\n    if obj.type == 'MESH':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# Delete all lights\nfor obj in list(bpy.data.objects):\n    if obj.type == 'LIGHT':\n        bpy.data.objects.remove(obj, do_unlink=True)\n\n# ==========================================\n# 2. CREATE THE JUPITER OBJECT\n# ==========================================\nbpy.ops.mesh.primitive_uv_sphere_add(\n    segments=128, \n    ring_count=64, \n    radius=27.0, \n    location=(0, 0, 0)\n)\njupiter = bpy.context.active_object\njupiter.name = "Jupiter_Model"\nbpy.ops.object.shade_smooth()\n\n# ==========================================\n# 3. ADD LIGHTING\n# ==========================================\n\n# Main Sun Light\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(30, 20, 20)\n)\nsun_light = bpy.context.active_object\nsun_light.name = "Sun_Light"\nsun_light.data.energy = 3.0\nsun_light.data.color = (1.0, 1.0, 0.95)\n\n# Fill Light\nbpy.ops.object.light_add(\n    type='SUN', \n    location=(-20, -10, -15)\n)\nfill_light = bpy.context.active_object\nfill_light.name = "Fill_Light"\nfill_light.data.energy = 1.0\nfill_light.data.color = (0.6, 0.7, 1.0)\n\n# ==========================================\n# 4. ANIMATE THE ROTATION\n# ==========================================\nbpy.context.scene.frame_start = 1\nbpy.context.scene.frame_end = 250\njupiter.rotation_mode = 'XYZ'\n\noriginal_interp = bpy.context.preferences.edit.keyframe_new_interpolation_type\nbpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n\n# Insert keyframes\nbpy.context.scene.frame_set(1)\njupiter.rotation_euler = (0, 0, 0)\njupiter.keyframe_insert(data_path="rotation_euler", index=2, frame=1)\n\nbpy.context.scene.frame_set(250)\njupiter.rotation_euler = (0, 0, math.radians(360))\njupiter.keyframe_insert(data_path="rotation_euler", index=2, frame=250)\n\nbpy.context.preferences.edit.keyframe_new_interpolation_type = original_interp\nbpy.context.scene.frame_set(1)\n\nprint("✅ Jupiter created!")`,
    saturn: `import bpy\nimport math\n\n# ==========================================\n# CONFIG\n# ==========================================\nPLANET_NAME = "Saturn"\nSPIN_FRAMES = 240\nFPS = 24\n\n# ==========================================\n# SET UP SCENE\n# ==========================================\nscene = bpy.context.scene\nscene.render.fps = FPS\nscene.frame_start = 1\nscene.frame_end = SPIN_FRAMES\n\n# ==========================================\n# GET SATURN MODEL\n# ==========================================\nif PLANET_NAME not in bpy.data.objects:\n    print(f"❌ Object '{PLANET_NAME}' not found!")\nelse:\n    saturn = bpy.data.objects[PLANET_NAME]\n    saturn.rotation_mode = 'XYZ'\n    \n    # ==========================================\n    # ANIMATE SPIN\n    # ==========================================\n    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'\n    \n    scene.frame_set(1)\n    saturn.rotation_euler = (0, 0, 0)\n    saturn.keyframe_insert(data_path="rotation_euler", frame=1)\n    \n    scene.frame_set(SPIN_FRAMES)\n    saturn.rotation_euler = (0, 0, math.radians(360))\n    saturn.keyframe_insert(data_path="rotation_euler", frame=SPIN_FRAMES)\n    \n    scene.frame_set(1)\n    print("✅ Saturn animation created!")`,
    uranus: `import bpy\nimport math\n\n# ==========================================\n# CONFIG\n# ==========================================\nPLANET_NAME = "Uranus"\nRING_NAME = "Uranus_Rings"\nSPIN_FRAMES = 240\nFPS = 24\n\nRING_INNER = 18.0\nRING_OUTER = 26.0\nRING_THICKNESS = 0.1\nRING_TILT = math.radians(82)  # Uranus rings are nearly vertical\n\n# ==========================================\n# SET UP SCENE\n# ==========================================\nscene = bpy.context.scene\nscene.render.fps = FPS\nscene.frame_start = 1\nscene.frame_end = SPIN_FRAMES\n\n# Remove existing ring if present\nif RING_NAME in bpy.data.objects:\n    bpy.data.objects.remove(bpy.data.objects[RING_NAME], do_unlink=True)\n\n# ==========================================\n# GET URANUS\n# ==========================================\nif PLANET_NAME not in bpy.data.objects:\n    print(f"❌ Object '{PLANET_NAME}' not found!")\nelse:\n    uranus = bpy.data.objects[PLANET_NAME]\n    \n    # ==========================================\n    # CREATE RINGS (TORUS)\n    # ==========================================\n    bpy.ops.mesh.primitive_torus_add(\n        major_radius=(RING_INNER + RING_OUTER) / 2,\n        minor_radius=(RING_OUTER - RING_INNER) / 2,\n        location=(0, 0, 0)\n    )\n    rings = bpy.context.active_object\n    rings.name = RING_NAME\n    rings.scale.z = RING_THICKNESS\n    rings.rotation_euler = (RING_TILT, 0, 0)\n    \n    # ==========================================\n    # RING MATERIAL\n    # ==========================================\n    ring_mat = bpy.data.materials.new(name="UranusRingMaterial")\n    ring_mat.use_nodes = True\n    nodes = ring_mat.node_tree.nodes\n    links = ring_mat.node_tree.links\n    \n    for n in nodes:\n        nodes.remove(n)\n    \n    r_out = nodes.new("ShaderNodeOutputMaterial")\n    r_bsdf = nodes.new("ShaderNodeBsdfPrincipled")\n    r_tex = nodes.new("ShaderNodeTexNoise")\n    r_ramp = nodes.new("ShaderNodeValToRGB")\n    r_coord = nodes.new("ShaderNodeTexCoord")\n    \n    links.new(r_coord.outputs["Generated"], r_tex.inputs["Vector"])\n    links.new(r_tex.outputs["Fac"], r_ramp.inputs["Fac"])\n    links.new(r_ramp.outputs["Color"], r_bsdf.inputs["Base Color"])\n    links.new(r_bsdf.outputs["BSDF"], r_out.inputs["Surface"])\n    \n    rings.data.materials.append(ring_mat)\n    print("✅ Uranus rings created!")`,
    neptune: `# Neptune Python Script for Blender\nimport bpy\n\n# Planet parameters\nname = "Neptune"\nradius = 3.88\ndistance = 449.7\nrotation_speed = 0.012\n\n# Create sphere\nbpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))\nobj = bpy.context.active_object\nobj.name = name`,
    pluto: `# Pluto Python Script for Blender\nimport bpy\n\n# Planet parameters\nname = "Pluto"\nradius = 0.18\ndistance = 590.6\nrotation_speed = 0.005\n\n# Create sphere\nbpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(distance, 0, 0))\nobj = bpy.context.active_object\nobj.name = name`
};

/**
 * Toggles the script modal visibility and populates content
 */
function toggleScript(id) {
    const modal = document.getElementById('scriptModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalScriptContent');
    
    if (!modal || !modalTitle || !modalContent) return;

    const name = id === 'sun' ? 'THE SUN' : id.toUpperCase();
    modalTitle.innerText = `${name} - BLENDER SCRIPT`;
    modalContent.innerText = scripts[id] || '# Script unavailable';
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

/**
 * Closes the script modal
 */
function closeModal() {
    const modal = document.getElementById('scriptModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    }
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('scriptModal');
    if (event.target == modal) {
        closeModal();
    }
});

// Planetary Age Calculation Data
const planetaryData = [
    { name: 'Mercury', ratio: 0.24 },
    { name: 'Venus', ratio: 0.615 },
    { name: 'Earth', ratio: 1.0 },
    { name: 'Mars', ratio: 1.88 },
    { name: 'Jupiter', ratio: 11.86 },
    { name: 'Saturn', ratio: 29.46 },
    { name: 'Uranus', ratio: 84 },
    { name: 'Neptune', ratio: 164.8 },
    { name: 'Pluto', ratio: 248 }
];

// Initialize calculator on page load
document.addEventListener('DOMContentLoaded', function() {
    const calculateBtn = document.getElementById('calculateBtn');
    const ageInput = document.getElementById('ageInput');
    const grid = document.getElementById('planetAges');

    if (calculateBtn && ageInput && grid) {
        calculateBtn.addEventListener('click', function() {
            const earthAge = parseFloat(ageInput.value);
            if (isNaN(earthAge) || earthAge <= 0) return;
            
            grid.innerHTML = '';
            planetaryData.forEach(p => {
                const age = (earthAge / p.ratio).toFixed(2);
                const col = document.createElement('div');
                col.className = 'col-6 col-sm-4 reveal-up';
                col.innerHTML = `
                    <div class="p-3 border border-thin bg-surface">
                        <div class="planet-name-calc small mb-1">${p.name.toUpperCase()}</div>
                        <div class="age-value-calc fs-5">${age} <span class="small text-dim">YRS</span></div>
                    </div>
                `;
                grid.appendChild(col);
            });
        });
    }
});
