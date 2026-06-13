"""
Main.py -- Beach Generator
=======================================
Digim 131 Final | Author: Hanan Daher
Assembles a basic beach environment from configuration data
using the Builders dispatcher pattern.

How to run:
  1. Open Maya
  2. Open Script Editor  (Windows > General Editors > Script Editor)
  3. Set the tab to Python
  4. Paste this file (or use  exec(open('/path/to/Main.py').read()) )
  5. Call:  build_beach()
"""

import os
import sys

import maya.cmds as cmds

# ---------------------------------------------------------------------------
# Make sure the folder containing this file is on sys.path so we can import
# the sibling modules (beach_geometry, beach_materials).
# ---------------------------------------------------------------------------
try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Inside Maya's Script Editor __file__ doesn't exist; fall back to
    # the project root directory.
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import beach_geometry as geo
import beach_materials as mat

# ---------------------------------------------------------------------------
# Scene-level constants
# ---------------------------------------------------------------------------

SAND_LENGTH = 60        # half-size of the sand/water planes

# ---------------------------------------------------------------------------
# Material Palette
# "key": (shader_name, (R, G, B))
# ---------------------------------------------------------------------------
MATERIAL_PALETTE = {
    "sand":    ("sand_mat",    (0.86, 0.79, 0.55)),
    "water":   ("water_mat",   (0.10, 0.45, 0.65)),
    "trunk":   ("trunk_mat",   (0.42, 0.26, 0.12)),
    "leaves":  ("leaves_mat",  (0.18, 0.55, 0.18)),
    "shell":   ("shell_mat",   (0.95, 0.88, 0.75)),
}

# ---------------------------------------------------------------------------
# Map each element "type" to which material key it should receive
# ---------------------------------------------------------------------------
TYPE_MATERIALS = {
    "sand":      "sand",
    "water":     "water",
    "trunk":     "trunk",
    "leaves":    "leaves",
    "seashell":  "shell",
}

# ---------------------------------------------------------------------------
# Builders dispatcher
# Maps element type string -> geometry function
# ---------------------------------------------------------------------------
BUILDERS = {
    "sand":     geo.create_sand,
    "water":    geo.create_water,
    "trunk":    geo.create_palmtree,
    "leaves":   geo.create_palmtree,
    "seashell": geo.create_seashells,
}

# ---------------------------------------------------------------------------
# Beach Configuration
# Each dict defines one element.  "type" picks the builder; the rest are
# keyword arguments forwarded to that function.
# Add more entries here to populate your scene — no code changes needed.
# ---------------------------------------------------------------------------
BEACH_CONFIG = [
    # ---- Ground ----
    {
        "type":     "sand",
        "width":    60,
        "length":   60,
        "position": (0, 0, 0),
    },

    # ---- Ocean ----
    {
        "type":     "water",
        "width":    60,
        "length":   40,
        "position": (0, 0.05, 30),
    },

    # ---- Palm Tree 1 ----
    {
        "type":     "trunk",
        "width":    1,
        "height":   12,
        "scale":    1.0,
        "length":   1,
        "position": (8, 0, -5),
        "axis":     "y",
    },
    {
        "type":     "leaves",
        "width":    1,
        "height":   12,
        "scale":    1.0,
        "length":   8,
        "position": (8, 0, -5),
        "axis":     "y",
    },

    # ---- Palm Tree 2 (taller, offset) ----
    {
        "type":     "trunk",
        "width":    1,
        "height":   15,
        "scale":    1.0,
        "length":   1,
        "position": (-10, 0, -8),
        "axis":     "y",
    },
    {
        "type":     "leaves",
        "width":    1,
        "height":   15,
        "scale":    1.1,
        "length":   9,
        "position": (-10, 0, -8),
        "axis":     "y",
    },

    # ---- Seashell clusters ----
    {
        "type":     "seashell",
        "width":    0.5,
        "height":   0.3,
        "scale":    1.0,
        "position": (3, 0, 5),
        "axis":     "y",
    },
    {
        "type":     "seashell",
        "width":    0.4,
        "height":   0.25,
        "scale":    0.8,
        "position": (-5, 0, 8),
        "axis":     "y",
    },
]

# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def create_element(data):
    """Dispatch one config entry to the correct builder function.

    Looks up data["type"] in BUILDERS and calls the matching function
    with the remaining keys as **keyword arguments.

    Args:
        data (dict): One entry from BEACH_CONFIG.  Must have a "type" key.

    Returns:
        str or None: The created Maya node name, or None if it failed.
    """
    element_type = data.get("type")

    # Validate: entry has a type
    if not element_type:
        cmds.warning("Config entry missing 'type' key -- skipping.")
        return None

    # Validate: we have a builder for this type
    builder = BUILDERS.get(element_type)
    if not builder:
        cmds.warning("Unknown element type '{}' -- skipping.".format(element_type))
        return None

    # Strip "type" before ** unpacking — it's not a geometry function parameter
    params = {k: v for k, v in data.items() if k != "type"}

    try:
        return builder(**params)
    except TypeError as error:
        cmds.warning("Bad params for type '{}': {}".format(element_type, error))
        return None


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def build_beach(config=None):
    """Build a complete beach scene from a list of config dicts.

    Args:
        config (list): List of element dicts.  Defaults to BEACH_CONFIG.

    Returns:
        list: Names of all Maya nodes that were created.
    """
    if config is None:
        config = BEACH_CONFIG

    # Fresh scene
    cmds.file(new=True, force=True)

    # -- Create materials --
    shaders = {}
    for key, (name, color) in MATERIAL_PALETTE.items():
        # Use the simple lambert helper so we only need beach_materials.py
        shader = cmds.shadingNode("lambert", asShader=True, name=name)
        sg = cmds.sets(
            renderable=True, noSurfaceShader=True,
            empty=True, name=name + "_SG"
        )
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
        cmds.setAttr(
            shader + ".color",
            color[0], color[1], color[2],
            type="double3"
        )
        shaders[key] = shader

    results = []

    # -- Build every element in the config list --
    for entry in config:
        obj = create_element(entry)

        if obj:
            # Auto-assign material based on element type
            mat_key = TYPE_MATERIALS.get(entry.get("type"))
            if mat_key and mat_key in shaders:
                mat.assign_material(obj, shaders[mat_key])
            results.append(obj)

    # Frame everything in the viewport
    cmds.viewFit(allObjects=True)

    print("=== Beach Complete ===")
    print("  {} elements created from {} config entries.".format(
        len(results), len(config)
    ))

    return results


# ---------------------------------------------------------------------------
# Auto-run when sourced directly in Maya's Script Editor
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_beach()