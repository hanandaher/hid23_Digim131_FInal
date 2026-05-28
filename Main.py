"""
main.py -- Beach Generator (W7)
=======================================
Digim 131 - Week 7 | Author: Hanan

Assembles a basic beach environment from configuration data using the Builders dispatcher pattern
"""

import os
import sys
import maya.cmds as cmds

try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

    if _THIS_DIR not in sys.path:
        sys.path.insert(0, _THIS_DIR)

import beach_geometry as geo
import beach_materials as mat


# ---------------------------------------------------------------------------
# Configuration Data
# ---------------------------------------------------------------------------
# Each dict is a "recipe" for one beach element.
# "type" tells the dispatcher WHICH function to call.
# The rest are parameters for that function.
# Add a new element = add one dict. No code changes needed.


config = {

    # SAND
"sand": {
    "width": 60,
    "height": 60,
    "position": (0,0,0)
},

    # WATER
"water": {
    "width": 60,
    "height": 60,
    "position": (0,0,10)
},

    # PALM TREE LEAVES
"leaves": {
    "width": 15,
    "height": 20,
    "scale": 15,
    "length": 15,
    "position": (5,15,2)
},

   # PALM TREE TRUNK
"trunk": {
    "width": 10,
    "height": 15,
    "scale": 15,
    "length": 10,
    "position": (5,0,2)
},

    # SEASHELLS
"seashell": {
    "width": .5,
    "height": .2,
    "scale": 1,
    "position": (3,0,1)

},

}

# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
def create_element(data):
    """Dispatch one config entry to the correct builder function.

    Looks up data["type"] in BUILDERS and calls the matching function
    with the remaining keys as ** keyword arguments.

    Args:
        data (dict): One entry from FORTRESS_CONFIG. Must have a "type" key.

    Returns:
        str or None: The created Maya node name, or None if failed.
    """
    element_type = data.get("type")

    # Check: does the entry have a type?
    if not element_type:
        cmds.warning("Config entry missing 'type' key -- skipping.")
        return None

    # Check: do we have a builder for this type?
    builder = BUILDERS.get(element_type)
    if not builder:
        cmds.warning("Unknown type '{}' -- skipping.".format(element_type))
        return None

    # Strip "type" before ** unpacking -- it's not a function parameter
    params = {k: v for k, v in data.items() if k != "type"}

    try:
        return builder(**params)
    except TypeError as error:
        cmds.warning("Bad params for '{}': {}".format(element_type, error))
        return None
# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def build_beach(config=None):
    """Build a complete beach from configuration data.

    Args:
        config (list): List of config dicts. Defaults to BEACH_CONFIG.

    Returns:
        list: Names of all created Maya nodes.
    """
    if config is None:
        config = BEACH_CONFIG

    cmds.file(new=True, force=True)

    # Create materials
    shaders = {}
    for key, (name, color) in MATERIAL_PALETTE.items():
        shaders[key] = mat.create_material(name, color)

    # Ground plane
    ground = cmds.polyPlane(
        w=SAND_LENGHT * 2, h=SAND_LENGTH * 2,
        sx=1, sy=1, name="sand_ground_#"
    )[0]

    results = [ground]

    # Process every entry in the config
    for entry in config:
        obj = create_element(entry)
        if obj:
            # Auto-assign material based on type
            mat_key = TYPE_MATERIALS.get(entry.get("type"))
            if mat_key and mat_key in shaders:
                mat.assign_material(obj, shaders[mat_key])
            results.append(obj)

    cmds.viewFit(allObjects=True)
    print("=== Beach Complete ===")
    print("  {} elements from {} config entries.".format(
        len(results), len(config)))







