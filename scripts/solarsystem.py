import bpy
import math
import os
import random

# ============================================================
# CONFIGURATION
# ============================================================
TEXTURE_DIR = r"C:\Users\PCA924~1\AppData\Local\Temp\solarsystem\tex"
RENDER_ENGINE = "BLENDER_EEVEE"
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
FRAME_START = 1
FRAME_END = 1500
USE_BLOOM = True

# ============================================================
# UTILITIES
# ============================================================
def resolve_asset_path(filename):
    return os.path.join(TEXTURE_DIR, filename)

def fetch_surface_map(pname):
    return resolve_asset_path(f"{pname.lower()}.jpg")

def set_interp(obj, mode='LINEAR'):
    ad = getattr(obj, "animation_data", None)
    if not ad:
        return
    act = getattr(ad, "action", None)
    if not act:
        return
    fcurves = getattr(act, "fcurves", None)
    if not fcurves:
        return
    for fc in fcurves:
        for kf in fc.keyframe_points:
            kf.interpolation = mode

# ============================================================
# SCENE SETUP
# ============================================================
def build_environment():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat, do_unlink=True)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)

    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.render.engine = RENDER_ENGINE
    scene.render.resolution_x = RESOLUTION_X
    scene.render.resolution_y = RESOLUTION_Y
    scene.render.film_transparent = False

    if scene.render.engine == "BLENDER_EEVEE":
        eevee = scene.eevee
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = USE_BLOOM
            if hasattr(eevee, "bloom_intensity"):
                eevee.bloom_intensity = 0.6
            if hasattr(eevee, "bloom_threshold"):
                eevee.bloom_threshold = 0.7
            if hasattr(eevee, "bloom_radius"):
                eevee.bloom_radius = 6.0
        if hasattr(eevee, "use_ssr"):
            eevee.use_ssr = True
        if hasattr(eevee, "use_soft_shadows"):
            eevee.use_soft_shadows = True
        if hasattr(eevee, "shadow_cube_size"):
            eevee.shadow_cube_size = '1024'
        if hasattr(eevee, "taa_render_samples"):
            eevee.taa_render_samples = 64

    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    wnt = world.node_tree
    wnt.nodes.clear()

    bg = wnt.nodes.new("ShaderNodeBackground")
    out = wnt.nodes.new("ShaderNodeOutputWorld")
    out.location = (320, 0)

    noise = wnt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-620, 160)
    noise.inputs["Scale"].default_value = 1.2
    noise.inputs["Detail"].default_value = 15.0
    noise.inputs["Roughness"].default_value = 0.55

    ramp = wnt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-420, 160)
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.05, 0.005, 0.01, 1)
    ramp.color_ramp.elements.new(0.85)
    ramp.color_ramp.elements[2].color = (0.15, 0.05, 0.01, 1)

    mix = wnt.nodes.new("ShaderNodeMixRGB")
    mix.location = (-180, 0)
    mix.blend_type = 'ADD'
    mix.inputs[0].default_value = 1.0

    stars = resolve_asset_path("stars.jpg")
    if os.path.exists(stars):
        tc = wnt.nodes.new("ShaderNodeTexCoord")
        mp = wnt.nodes.new("ShaderNodeMapping")
        env = wnt.nodes.new("ShaderNodeTexEnvironment")
        tc.location = (-820, -200)
        mp.location = (-620, -200)
        env.location = (-420, -200)
        try:
            env.image = bpy.data.images.load(stars)
        except Exception:
            pass
        wnt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
        wnt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
        wnt.links.new(env.outputs["Color"], mix.inputs[1])
    else:
        mix.inputs[1].default_value = (0, 0, 0, 1)

    wnt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    wnt.links.new(ramp.outputs["Color"], mix.inputs[2])
    wnt.links.new(mix.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.5
    wnt.links.new(bg.outputs["Background"], out.inputs["Surface"])

# ============================================================
# MATERIALS
# ============================================================
def make_surface_shader(name, texture_path, roughness=0.8, metallic=0.0, fallback_color=(0.5,0.5,0.5,1)):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    out.location = (620, 0)
    bsdf.location = (240, 0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    coord = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    img = nodes.new("ShaderNodeTexImage")
    coord.location = (-700, 0)
    mapping.location = (-500, 0)
    img.location = (-260, 0)

    links.new(coord.outputs["UV"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], img.inputs["Vector"])

    loaded = False
    if texture_path and os.path.exists(texture_path):
        try:
            img.image = bpy.data.images.load(texture_path, check_existing=True)
            loaded = True
        except Exception:
            loaded = False

    if loaded:
        links.new(img.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = fallback_color

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat

def make_solid_mat(name, color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

def make_star_shader():
    mat = bpy.data.materials.new(name="Sun_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    out.location = (620, 0)
    emit.location = (260, 0)
    emit.inputs["Strength"].default_value = 12.0
    emit.inputs["Color"].default_value = (1.0, 0.55, 0.15, 1.0)

    sun_tex = resolve_asset_path("sun.jpg")
    if os.path.exists(sun_tex):
        coord = nodes.new("ShaderNodeTexCoord")
        mapping = nodes.new("ShaderNodeMapping")
        img = nodes.new("ShaderNodeTexImage")
        mul = nodes.new("ShaderNodeMixRGB")

        coord.location = (-760, 0)
        mapping.location = (-560, 0)
        img.location = (-340, 0)
        mul.location = (-80, 40)
        mul.blend_type = 'MULTIPLY'
        mul.inputs["Fac"].default_value = 0.75
        mul.inputs["Color2"].default_value = (1.0, 0.72, 0.25, 1.0)

        try:
            img.image = bpy.data.images.load(sun_tex, check_existing=True)
            links.new(coord.outputs["UV"], mapping.inputs["Vector"])
            links.new(mapping.outputs["Vector"], img.inputs["Vector"])
            links.new(img.outputs["Color"], mul.inputs["Color1"])
            links.new(mul.outputs["Color"], emit.inputs["Color"])
        except Exception:
            pass

    links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat

def make_disc_shader():
    mat = bpy.data.materials.new(name="Ring_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    out.location = (620, 0)
    bsdf.location = (240, 0)
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Alpha"].default_value = 0.65
    bsdf.inputs["Base Color"].default_value = (0.85, 0.78, 0.65, 1.0)

    mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat

# ============================================================
# OBJECT HELPERS
# ============================================================
def add_globe(name, radius, location=(0,0,0), segments=64, rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    return obj

def add_flat_ring(name, radius, location=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=radius, depth=0.001, location=location)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    return obj

def add_anchor(name, location=(0,0,0)):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_light_source(name, location, energy, radius=0.5, color=(1, 0.9, 0.7)):
    bpy.ops.object.light_add(type='POINT', location=location)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.data.shadow_soft_size = radius
    return light

def assign_shader(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# ============================================================
# INLINE SATELLITE BUILDER
# ============================================================
def generate_satellite_in_scene(orbit_r, pivot_obj, scale_factor):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    root = bpy.context.active_object
    root.name = "Satellite_Root"

    mat_body  = make_solid_mat("SAT_Body_Mat",  color=(0.75, 0.77, 0.80, 1), metallic=0.35, roughness=0.35)
    mat_panel = make_solid_mat("SAT_Panel_Mat", color=(0.08, 0.14, 0.28, 1), metallic=0.05, roughness=0.25)
    mat_frame = make_solid_mat("SAT_Frame_Mat", color=(0.15, 0.15, 0.16, 1), metallic=0.55, roughness=0.3)
    mat_dish  = make_solid_mat("SAT_Dish_Mat",  color=(0.85, 0.85, 0.86, 1), metallic=0.15, roughness=0.4)

    def new_cube(name, size, loc):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = size
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return obj

    def new_cyl(name, radius, depth, loc, rot=(0,0,0)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc, rotation=rot)
        obj = bpy.context.active_object
        obj.name = name
        return obj

    body = new_cube("SAT_Body", size=(0.55, 0.35, 0.30), loc=(0,0,0)); body.data.materials.append(mat_body); body.parent = root
    nose = new_cube("SAT_Nose", size=(0.18, 0.20, 0.16), loc=(0.55, 0, 0)); nose.data.materials.append(mat_frame); nose.parent = root
    mast = new_cyl("SAT_Mast", radius=0.02, depth=0.5, loc=(0.0, 0.0, 0.42), rot=(math.radians(90),0,0)); mast.data.materials.append(mat_frame); mast.parent = root
    
    dish = new_cyl("SAT_Dish", radius=0.20, depth=0.03, loc=(0.72, 0, 0), rot=(0, math.radians(90), 0)); dish.data.materials.append(mat_dish); dish.parent = root
    arm_l = new_cube("SAT_Arm_L", size=(0.45, 0.03, 0.03), loc=(0, 0.40, 0)); arm_l.data.materials.append(mat_frame); arm_l.parent = root
    arm_r = new_cube("SAT_Arm_R", size=(0.45, 0.03, 0.03), loc=(0, -0.40, 0)); arm_r.data.materials.append(mat_frame); arm_r.parent = root
    panel_l = new_cube("SAT_Panel_L", size=(0.95, 0.30, 0.02), loc=(0, 0.90, 0)); panel_l.data.materials.append(mat_panel); panel_l.parent = root
    panel_r = new_cube("SAT_Panel_R", size=(0.95, 0.30, 0.02), loc=(0, -0.90, 0)); panel_r.data.materials.append(mat_panel); panel_r.parent = root

    root.location = (orbit_r, 0, 0)
    root.scale = (scale_factor, scale_factor, scale_factor)
    root.parent = pivot_obj
    return root

# ============================================================
# DATA
# ============================================================
PLANET_DATA = [
    ("Mercury", 0.11, 12, 88, 58, 0.03, (0.6, 0.5, 0.45, 1)),
    ("Venus",   0.28, 18, 225, 243, 177.4, (0.9, 0.8, 0.5, 1)),
    ("Earth",   0.30, 25, 365, 1, 23.4, (0.2, 0.5, 0.9, 1)),
    ("Mars",    0.16, 34, 687, 1.03, 25.2, (0.8, 0.4, 0.2, 1)),
    ("Jupiter", 3.36, 55, 4333, 0.41, 3.1, (0.8, 0.7, 0.55, 1)),
    ("Saturn",  2.83, 80, 10759, 0.45, 26.7, (0.9, 0.85, 0.6, 1)),
    ("Uranus",  1.20, 105, 30688, 0.72, 97.8, (0.5, 0.85, 0.9, 1)),
    ("Neptune", 1.16, 125, 60182, 0.67, 28.3, (0.2, 0.4, 0.9, 1)),
    ("Pluto",   0.05, 150, 90560, 6.39, 122.5, (0.6, 0.5, 0.4, 1)),
]

SUN_RADIUS = 8.0
SPEED_SCALE = 1.5

# ============================================================
# BUILD SYSTEM
# ============================================================
def build_system():
    planets = {}

    sun_obj = add_globe("Sun", SUN_RADIUS)
    assign_shader(sun_obj, make_star_shader())

    sun_light = add_light_source("SunLight", (0, 0, 0), energy=200000, radius=SUN_RADIUS, color=(1.0, 0.95, 0.9))
    sun_light.data.use_shadow = False
    sun_light.data.use_custom_distance = True
    sun_light.data.cutoff_distance = 600.0

    bpy.ops.object.light_add(type='SUN', rotation=(math.radians(35), math.radians(30), 0))
    fill_a = bpy.context.active_object
    fill_a.name = "FillA"
    fill_a.data.energy = 0.08
    fill_a.data.color = (0.55, 0.65, 1.0)
    fill_a.data.use_shadow = False

    bpy.ops.object.light_add(type='SUN', rotation=(math.radians(-40), math.radians(-140), 0))
    fill_b = bpy.context.active_object
    fill_b.name = "FillB"
    fill_b.data.energy = 0.05
    fill_b.data.color = (1.0, 0.9, 0.8)
    fill_b.data.use_shadow = False

    for (pname, prad, orbit_r, orb_period, rot_period, axial_tilt, base_color) in PLANET_DATA:
        pivot = add_anchor(f"{pname}_Pivot")
        planet = add_globe(pname, prad, location=(orbit_r, 0, 0))
        planet.parent = pivot
        planet.rotation_euler.x = math.radians(axial_tilt)

        tpath = fetch_surface_map(pname)
        mat = make_surface_shader(f"{pname}_Mat", tpath, roughness=0.85, metallic=0.0, fallback_color=base_color)
        assign_shader(planet, mat)

        planets[pname] = {"pivot": pivot, "planet": planet, "orbit_r": orbit_r, "radius": prad, "base_color": base_color}

    sat_obj = planets["Saturn"]["planet"]
    sat_r = planets["Saturn"]["radius"]
    ring = add_flat_ring("Saturn_Ring", radius=sat_r * 2.2, location=(0, 0, 0))
    ring.parent = sat_obj
    assign_shader(ring, make_disc_shader())

    earth_obj = planets["Earth"]["planet"]
    earth_r = planets["Earth"]["radius"]
    moon_radius = earth_r * 0.42
    moon_orbit_r = earth_r * 4.2

    moon_pivot = add_anchor("Moon_Pivot", location=(0, 0, 0))
    moon_pivot.parent = earth_obj

    moon = add_globe("Moon", moon_radius, location=(moon_orbit_r, 0, 0))
    moon.parent = moon_pivot
    
    moon_tex = resolve_asset_path("moon.jpg")
    moon_mat = make_surface_shader(
        "Moon_Mat",
        moon_tex,
        roughness=0.9,
        metallic=0.0,
        fallback_color=(0.75, 0.75, 0.78, 1.0)
    )
    assign_shader(moon, moon_mat)

    moon_pivot.rotation_euler = (0, 0, 0)
    moon_pivot.keyframe_insert(data_path="rotation_euler", frame=1)
    moon_pivot.rotation_euler.z = math.radians(360 * 13) 
    moon_pivot.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)
    set_interp(moon_pivot, 'LINEAR')

    sat_orbit_r = earth_r * 1.6
    sat_pivot = add_anchor("Satellite_Pivot")
    sat_pivot.parent = earth_obj
    sat_pivot.rotation_euler = (math.radians(28), 0, 0)

    sat_scale = earth_r * 0.25
    sat_body = generate_satellite_in_scene(sat_orbit_r, sat_pivot, sat_scale)

    sat_pivot.rotation_euler = (math.radians(28), 0, 0)
    sat_pivot.keyframe_insert(data_path="rotation_euler", frame=1)
    sat_pivot.rotation_euler = (math.radians(28), 0, math.radians(360 * 12))
    sat_pivot.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)
    set_interp(sat_pivot, 'LINEAR')

    sat_body.rotation_euler = (0, 0, 0)
    sat_body.keyframe_insert(data_path="rotation_euler", frame=1)
    sat_body.rotation_euler.y = math.radians(360 * 3)
    sat_body.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)
    set_interp(sat_body, 'LINEAR')

    return planets

# ============================================================
# ORBIT LINES
# ============================================================
def render_orbit_lines():
    mat = bpy.data.materials.new("Orbit_Line_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    em = nodes.new("ShaderNodeEmission")
    tr = nodes.new("ShaderNodeBsdfTransparent")
    mx = nodes.new("ShaderNodeMixShader")

    em.inputs["Color"].default_value = (0.55, 0.75, 1.0, 1.0)
    em.inputs["Strength"].default_value = 0.3
    mx.inputs[0].default_value = 0.85

    links.new(tr.outputs["BSDF"], mx.inputs[1])
    links.new(em.outputs["Emission"], mx.inputs[2])
    links.new(mx.outputs["Shader"], out.inputs["Surface"])

    mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"

    segs = 256
    for (pname, _, orbit_r, *_rest) in PLANET_DATA:
        cd = bpy.data.curves.new(name=f"Orbit_{pname}", type='CURVE')
        cd.dimensions = '3D'
        cd.bevel_depth = 0.015
        cd.use_fill_caps = True
        sp = cd.splines.new('POLY')
        sp.use_cyclic_u = True
        sp.points.add(segs - 1)
        for i, pt in enumerate(sp.points):
            a = (2 * math.pi * i) / segs
            pt.co = (orbit_r * math.cos(a), orbit_r * math.sin(a), 0.0, 1.0)
        ob = bpy.data.objects.new(f"Orbit_{pname}", cd)
        bpy.context.collection.objects.link(ob)
        ob.data.materials.append(mat)

# ============================================================
# ASTEROIDS (TEXTURED)
# ============================================================
def place_debris():
    root = add_anchor("AsteroidField_Root")

    mat = bpy.data.materials.new("Asteroid_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    out.location = (500, 0)
    bsdf.location = (200, 0)
    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Metallic"].default_value = 0.0

    ast_tex = resolve_asset_path("asteroid.jpg")
    if os.path.exists(ast_tex):
        tex = nodes.new("ShaderNodeTexImage")
        tex.location = (-300, 0)
        coord = nodes.new("ShaderNodeTexCoord")
        coord.location = (-700, 0)
        mapping = nodes.new("ShaderNodeMapping")
        mapping.location = (-500, 0)

        noise = nodes.new("ShaderNodeTexNoise")
        noise.location = (-500, -250)
        noise.inputs["Scale"].default_value = 8.0

        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.location = (-300, -250)
        ramp.color_ramp.elements[0].color = (0.75, 0.75, 0.75, 1.0)
        ramp.color_ramp.elements[1].color = (1.1, 1.1, 1.1, 1.0)

        mul = nodes.new("ShaderNodeMixRGB")
        mul.location = (-50, -120)
        mul.blend_type = 'MULTIPLY'
        mul.inputs["Fac"].default_value = 0.7

        try:
            tex.image = bpy.data.images.load(ast_tex, check_existing=True)
        except Exception as e:
            pass

        links.new(coord.outputs["UV"], mapping.inputs["Vector"])
        links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
        links.new(tex.outputs["Color"], mul.inputs["Color1"])
        links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], mul.inputs["Color2"])
        links.new(mul.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.35, 0.33, 0.30, 1.0)

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    count = 80
    for i in range(count):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.7)
        a = bpy.context.active_object
        a.name = f"Asteroid_{i:02d}"
        a.scale = (
            random.uniform(0.6, 2.0),
            random.uniform(0.6, 2.0),
            random.uniform(0.5, 1.8)
        )
        a.location = (
            random.uniform(20.0, 170.0) * math.cos(random.uniform(0, 2 * math.pi)),
            random.uniform(20.0, 170.0) * math.sin(random.uniform(0, 2 * math.pi)),
            random.uniform(-25.0, 25.0)
        )
        assign_shader(a, mat)
        a.parent = root

# ============================================================
# MOTION
# ============================================================
def run_motion(planets):
    for (pname, _, _, orb_period, _, axial_tilt, _) in PLANET_DATA:
        pivot = planets[pname]["pivot"]
        planet = planets[pname]["planet"]

        deg_per_frame = 360.0 / (orb_period / SPEED_SCALE)
        pivot.rotation_euler = (0, 0, 0)
        pivot.keyframe_insert(data_path="rotation_euler", frame=1)
        pivot.rotation_euler.z = math.radians(deg_per_frame * FRAME_END)
        pivot.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)
        set_interp(pivot, 'LINEAR')

        planet.rotation_euler = (math.radians(axial_tilt), 0, 0)
        planet.keyframe_insert(data_path="rotation_euler", frame=1)
        planet.rotation_euler = (math.radians(axial_tilt), 0, math.radians(0.5 * FRAME_END))
        planet.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)
        set_interp(planet, 'LINEAR')

# ============================================================
# LABELS
# ============================================================
def add_name_tags(planets, cam_obj, blocks):
    font_path = resolve_asset_path("spacegrotesk.ttf")
    label_nodes = {}

    for (pname, prad, orbit_r, _, _, _, base_color) in PLANET_DATA:
        pivot = planets[pname]["pivot"]
        lp = prad * 2.5 if pname == "Saturn" else prad

        rig = add_anchor(f"LabelRig_{pname}", location=(orbit_r, 0, 0))
        rig.parent = pivot
        t = rig.constraints.new(type='TRACK_TO')
        t.target = cam_obj
        t.track_axis = 'TRACK_Z'
        t.up_axis = 'UP_Y'

        bpy.ops.object.text_add(location=(0, 0, 0))
        txt = bpy.context.active_object
        txt.parent = rig
        txt.data.body = pname.upper()
        txt.data.size = lp * 0.35
        txt.data.align_x = 'LEFT'
        txt.location = (lp * 1.3, lp * 0.2, 0)
        if os.path.exists(font_path):
            try:
                txt.data.font = bpy.data.fonts.load(font_path)
            except Exception:
                pass

        m = bpy.data.materials.new(f"Label_{pname}_Mat")
        m.use_nodes = True
        m.blend_method = 'BLEND'
        n = m.node_tree.nodes
        l = m.node_tree.links
        n.clear()
        o = n.new("ShaderNodeOutputMaterial")
        em = n.new("ShaderNodeEmission")
        tr = n.new("ShaderNodeBsdfTransparent")
        mx = n.new("ShaderNodeMixShader")
        em.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        em.inputs["Strength"].default_value = 5.0
        mx.inputs[0].default_value = 0.0
        l.new(tr.outputs["BSDF"], mx.inputs[1])
        l.new(em.outputs["Emission"], mx.inputs[2])
        l.new(mx.outputs["Shader"], o.inputs["Surface"])
        txt.data.materials.append(m)
        label_nodes[pname] = mx

    for (pname, b_start, b_end) in blocks:
        mx = label_nodes[pname]
        mx.inputs[0].default_value = 0.0
        mx.inputs[0].keyframe_insert(data_path="default_value", frame=1)
        mx.inputs[0].keyframe_insert(data_path="default_value", frame=b_start + 5)
        mx.inputs[0].default_value = 1.0
        mx.inputs[0].keyframe_insert(data_path="default_value", frame=b_start + 20)
        mx.inputs[0].keyframe_insert(data_path="default_value", frame=b_end - 20)
        mx.inputs[0].default_value = 0.0
        mx.inputs[0].keyframe_insert(data_path="default_value", frame=b_end - 2)

# ============================================================
# CAMERA
# ============================================================
def setup_camera_rig(planets):
    cam_focus = add_anchor("CameraFocus")
    cam_rig = add_anchor("CameraRig")

    bpy.ops.object.camera_add(location=(0, -150, 40))
    cam = bpy.context.active_object
    cam.name = "MainCamera"
    bpy.context.scene.camera = cam
    cam.parent = cam_rig

    tr = cam.constraints.new(type='TRACK_TO')
    tr.target = cam_focus
    tr.track_axis = 'TRACK_NEGATIVE_Z'
    tr.up_axis = 'UP_Y'

    targets = {"Sun": bpy.data.objects.get("Sun")}
    for pname, *_ in PLANET_DATA:
        targets[pname] = planets[pname]["planet"]

    for k, tgt in targets.items():
        c1 = cam_rig.constraints.new(type='COPY_LOCATION')
        c1.name = f"Lock_{k}"
        c1.target = tgt
        c1.influence = 0.0

        c2 = cam_focus.constraints.new(type='COPY_LOCATION')
        c2.name = f"Lock_{k}"
        c2.target = tgt
        c2.influence = 0.0

    def lock(name, frame, inf):
        for o in (cam_rig, cam_focus):
            c = o.constraints.get(f"Lock_{name}")
            c.influence = inf
            c.keyframe_insert(data_path="influence", frame=frame)

    lock("Sun", 1, 1.0)
    lock("Sun", 200, 1.0)
    for pname, *_ in PLANET_DATA:
        lock(pname, 1, 0.0)
        lock(pname, 200, 0.0)

    cam.location = (0, -150, 40); cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (40, -130, 30); cam.keyframe_insert(data_path="location", frame=200)

    seq = [p[0] for p in PLANET_DATA]
    block = 1000 // len(seq)
    blocks = []
    prev = "Sun"

    for i, pname in enumerate(seq):
        bs = 200 + i * block
        be = 200 + (i + 1) * block if i < len(seq)-1 else 1200
        blocks.append((pname, bs, be))

        lock(prev, bs, 1.0); lock(prev, bs + 1, 0.0)
        lock(pname, bs, 0.0); lock(pname, bs + 16, 1.0); lock(pname, be, 1.0)

        r = planets[pname]["radius"]
        
        dist = max(r * 14.0, 0.8)
        height = max(r * 2.0, 0.2)

        q1 = bs + int((be - bs) * 0.5)

        cam.location = (dist, -dist, height); cam.keyframe_insert(data_path="location", frame=bs + 10)
        cam.location = (dist * 1.2, 0, height); cam.keyframe_insert(data_path="location", frame=q1)
        cam.location = (dist, dist, height); cam.keyframe_insert(data_path="location", frame=be)

        prev = pname

    lock(prev, 1200, 1.0); lock(prev, 1201, 0.0)
    lock("Sun", 1200, 0.0); lock("Sun", 1240, 1.0); lock("Sun", 1400, 1.0)
    cam.location = (80, -80, 30); cam.keyframe_insert(data_path="location", frame=1200)
    cam.location = (0, -60, 20); cam.keyframe_insert(data_path="location", frame=1400)

    lock("Sun", 1500, 1.0)
    cam.location = (0, -60, 20); cam.keyframe_insert(data_path="location", frame=1400)
    cam.location = (0, -250, 60); cam.keyframe_insert(data_path="location", frame=1500)

    set_interp(cam_rig, 'BEZIER')
    set_interp(cam_focus, 'BEZIER')
    set_interp(cam, 'BEZIER')

    return cam, blocks

# ============================================================
# MAIN
# ============================================================
def launch():
    print("[1/5] Scene")
    build_environment()
    print("[2/5] System")
    planets = build_system()
    print("[2b/5] Orbit lines")
    render_orbit_lines()
    print("[2c/5] Asteroids")
    place_debris()
    print("[3/5] Motion")
    run_motion(planets)
    print("[4/5] Camera")
    cam, blocks = setup_camera_rig(planets)
    print("[5/5] Labels")
    add_name_tags(planets, cam, blocks)
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    print("Done. Press SPACE to preview.")

launch()