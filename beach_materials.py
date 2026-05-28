import maya.cmds as cmds


def _make_sg(shader, name):
    """Create a shading group for a shader and connect it. Returns the SG."""
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    return sg


def assign_material(obj, shader):
    """Assign a shader to a transform/shape (finds or makes its shading group)."""
    sgs = cmds.listConnections(shader + ".outColor", type="shadingEngine")
    sg = sgs[0] if sgs else _make_sg(shader, shader)
    cmds.sets(obj, edit=True, forceElement=sg)
    return sg
def create_ocean_material(name="ocean_mat",
                          shallow=(0.0, 0.45, 0.55),
                          deep=(0.0, 0.12, 0.25),
                          wave_scale=8.0,
                          choppiness=1.0,
                          reflectivity=0.4):
    """Procedural water material: depth-graded colour + noise-driven wave bump."""
    if cmds.objExists(name):
        return name

    shader = cmds.shadingNode("blinn", asShader=True, name=name)
    _make_sg(shader, name)

    # colour: shallow (near shore) -> deep
    ramp = cmds.shadingNode("ramp", asTexture=True, name=name + "_depth")
    cmds.setAttr(ramp + ".colorEntryList[0].color", shallow[0], shallow[1], shallow[2], type="double3")
    cmds.setAttr(ramp + ".colorEntryList[0].position", 0.0)
    cmds.setAttr(ramp + ".colorEntryList[1].color", deep[0], deep[1], deep[2], type="double3")
    cmds.setAttr(ramp + ".colorEntryList[1].position", 1.0)
    cmds.connectAttr(ramp + ".outColor", shader + ".color", force=True)

    # waves: fractal -> bump
    place = cmds.shadingNode("place2dTexture", asUtility=True, name=name + "_place")
    cmds.setAttr(place + ".repeatU", wave_scale)
    cmds.setAttr(place + ".repeatV", wave_scale)
    fractal = cmds.shadingNode("fractal", asTexture=True, name=name + "_waves")
    cmds.setAttr(fractal + ".ratio", 0.7)
    cmds.connectAttr(place + ".outUV", fractal + ".uvCoord", force=True)
    cmds.connectAttr(place + ".outUvFilterSize", fractal + ".uvFilterSize", force=True)

    bump = cmds.shadingNode("bump2d", asUtility=True, name=name + "_bump")
    cmds.setAttr(bump + ".bumpDepth", 0.3 * choppiness)
    cmds.connectAttr(fractal + ".outAlpha", bump + ".bumpValue", force=True)
    cmds.connectAttr(bump + ".outNormal", shader + ".normalCamera", force=True)

    # watery surface qualities
    cmds.setAttr(shader + ".specularColor", 1, 1, 1, type="double3")
    cmds.setAttr(shader + ".eccentricity", 0.1)
    cmds.setAttr(shader + ".specularRollOff", 0.7)
    cmds.setAttr(shader + ".reflectivity", reflectivity)
    return shader
def create_ocean_material_builtin(name="ocean_mat",
                                  water_color=(0.0, 0.1, 0.2),
                                  wave_speed=1.0,
                                  num_frequencies=8.0,
                                  foam=0.4,
                                  wind_uv=(1.0, 0.0),
                                  scale=10.0):
    """Assign Maya's built-in procedural oceanShader (waves, foam, glints)."""
    if cmds.objExists(name):
        return name
    ocean = cmds.shadingNode("oceanShader", asShader=True, name=name)
    _make_sg(ocean, name)

    cmds.setAttr(ocean + ".waterColor", water_color[0], water_color[1], water_color[2], type="double3")
    cmds.setAttr(ocean + ".waveSpeed", wave_speed)
    cmds.setAttr(ocean + ".numFrequencies", num_frequencies)
    cmds.setAttr(ocean + ".foamThreshold", 1.0 - foam)   # lower threshold = more foam
    cmds.setAttr(ocean + ".foamOffset", 0.1)
    cmds.setAttr(ocean + ".windUV", wind_uv[0], wind_uv[1], type="double2")
    cmds.setAttr(ocean + ".scale", scale)
    # NOTE: overall wave size is a *ramp* input, tune via e.g.:
    #   cmds.setAttr(ocean + ".waveHeight[0].waveHeight_FloatValue", 0.8)
    return ocean