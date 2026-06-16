"""beach_ui_starter.py  -- UI starter for the Beach Generator.
=============================================================================
DIGM 131 -- Week 10

This is a LIGHTWEIGHT scaffold for the Week-10 UI on top of your existing
geometry builders in `beach_geometry.py`.

What's already done for you here:
    * `default_settings()`   -- the settings dict shape (sizes + counts + seed)
    * `do_the_work(settings)` -- builds a local config list and dispatches
                                 directly to your geometry builders.

What you fill in:
    * `build_ui()`     -- pick controls and lay them out
    * `read_settings()` -- query each control into the same dict shape

See UI_DESIGN.md for the suggested controls. The shape matches
`tool_skeleton.py` and the worked example in `demo_ui_and_polish.py`.

NOTE: this starter calls your geometry builders directly rather than going
through `Main.build_beach()` -- that driver currently references some
undefined names (BUILDERS, BEACH_CONFIG, MATERIAL_PALETTE, SAND_LENGTH,
TYPE_MATERIALS) and the module-level `config` is a dict rather than a list,
so it can't run yet. Once those are fixed (see UI_DESIGN.md "nice-to-have"),
switching `do_the_work()` over to call `Main.build_beach(config_list)` is a
one-line change.
"""

import os
import random
import sys

import maya.cmds as cmds

# Make sure this folder is on Maya's path so the imports below work whether
# you source this file or import it from the Script Editor.
try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

# Your existing geometry module -- DO NOT duplicate the logic, import it.
# (Requires the 'mport' -> 'import' fix from your open bug-fix PR.)
import beach_geometry as geo  # noqa: E402


# =====================================================================
# LAYER 3 -- LOGIC  (wired to your geometry builders; usually no edits)
# =====================================================================

# Local dispatcher table -- maps an entry's "type" to the matching builder.
# Once Main.py defines BUILDERS itself, you can swap this for
# `from Main import BUILDERS` (or just call Main.build_beach directly).
_LOCAL_BUILDERS = {
    "sand":     geo.create_sand,
    "water":    geo.create_water,
    "palmtree": geo.create_palmtree,
    "seashell": geo.create_seashells,
}


def default_settings():
    """The dict shape this tool consumes. Each key maps to one UI control."""
    return {
        "beach_size":    60.0,
        "palm_count":       3,
        "shell_patches":    2,
        "palm_scale":    15.0,
        "spread":        25.0,
        "seed":            42,
        "group_name":  "beach_grp",
    }


def _dispatch(entry):
    """Pull entry['type'] out and call the matching builder with the rest."""
    element_type = entry.get("type")
    builder = _LOCAL_BUILDERS.get(element_type)
    if not builder:
        cmds.warning("Unknown beach element type '{}' -- skipping.".format(element_type))
        return None
    params = {k: v for k, v in entry.items() if k != "type"}
    try:
        return builder(**params)
    except TypeError as error:
        cmds.warning("Bad params for '{}': {}".format(element_type, error))
        return None


def do_the_work(settings):
    """Turn the settings dict into a config list and build the beach."""
    beach_size    = settings.get("beach_size", 60.0)
    palm_count    = settings.get("palm_count", 3)
    shell_patches = settings.get("shell_patches", 2)
    palm_scale    = settings.get("palm_scale", 15.0)
    spread        = settings.get("spread", 25.0)
    seed          = settings.get("seed", 42)

    if beach_size <= 0:
        raise ValueError("beach_size must be > 0, got {}".format(beach_size))
    if spread <= 0:
        raise ValueError("spread must be > 0, got {}".format(spread))

    rng = random.Random(seed)

    config_list = []

    # Sand + water (the two big planes)
    config_list.append({
        "type": "sand",
        "width": beach_size,
        "length": beach_size,
        "position": (0, 0, 0),
    })
    config_list.append({
        "type": "water",
        "width": beach_size,
        "length": beach_size,
        "position": (0, 0.05, beach_size * 0.25),
    })

    # Scattered palms
    for _ in range(palm_count):
        config_list.append({
            "type": "palmtree",
            "width": 10,
            "height": 15,
            "scale": palm_scale,
            "length": 15,
            "position": (rng.uniform(-spread, spread), 0,
                         rng.uniform(-spread, spread)),
        })

    # Scattered shell patches
    for _ in range(shell_patches):
        config_list.append({
            "type": "seashell",
            "width": 0.5,
            "height": 0.2,
            "scale": 1.0,
            "position": (rng.uniform(-spread, spread), 0,
                         rng.uniform(-spread, spread)),
        })

    created = [_dispatch(entry) for entry in config_list]

    real_nodes = [c for c in created if c]
    if real_nodes:
        cmds.group(real_nodes, name=settings.get("group_name", "beach_grp"))
    return real_nodes


# =====================================================================
# LAYER 1 -- UI  (TODO: YOU fill this in)
# =====================================================================

_ui = {}   # registry: control names keyed by settings-dict key


def build_ui():
    """Draw the Beach Generator window.

    TODO -- fill this in. For each setting in default_settings(), add a
    control and store its name in _ui[<setting_key>]. See UI_DESIGN.md
    for the suggested controls; the shape to mirror lives in
    tool_skeleton.py and demo_ui_and_polish.py.
    """
    window = "beachGenWin"
    if cmds.window(window, exists=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Beach Generator", widthHeight=(380, 360))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6,
                      columnOffset=("both", 14))
    cmds.text(label="Set the beach size + counts, then press Build.",
              align="left")

    # TODO -- add controls for each key in default_settings(). For example:
    #   _ui["beach_size"] = cmds.floatSliderGrp(
    #       label="Beach size", field=True, min=20.0, max=120.0, value=60.0)
    #   _ui["palm_count"] = cmds.intSliderGrp(
    #       label="Palms", field=True, min=0, max=10, value=3)
    #   _ui["shell_patches"] = cmds.intSliderGrp(
    #       label="Shell patches", field=True, min=0, max=6, value=2)
    #   _ui["seed"] = cmds.intFieldGrp(label="Seed", value1=42)
    #   _ui["group_name"] = cmds.textFieldGrp(label="Group name", text="beach_grp")

    cmds.button(label="Build beach", height=32, command=lambda *_: on_run())
    cmds.showWindow(window)


# =====================================================================
# LAYER 2 -- DATA + BRIDGE
# =====================================================================

def read_settings():
    """Query every control and return the dict shape from default_settings().

    TODO -- for each key in default_settings(), query _ui[<key>] with
    `query=True`. Examples:
        "beach_size":    cmds.floatSliderGrp(_ui["beach_size"], query=True, value=True),
        "palm_count":    cmds.intSliderGrp(_ui["palm_count"], query=True, value=True),
        "shell_patches": cmds.intSliderGrp(_ui["shell_patches"], query=True, value=True),
        "seed":          cmds.intFieldGrp(_ui["seed"], query=True, value1=True),
        "group_name":    cmds.textFieldGrp(_ui["group_name"], query=True, text=True),
    """
    # Placeholder so partial code still runs while you're filling this in.
    # Replace this with the real queries once your controls exist.
    return default_settings()


def on_run():
    """Bridge: gather settings, hand to logic, surface errors politely."""
    settings = read_settings()
    try:
        created = do_the_work(settings)
        print("[BeachGen] built {} objects with {}".format(len(created), settings))
    except ValueError as error:
        cmds.warning("Could not build: {}".format(error))


# =====================================================================
# RUN
# =====================================================================

if __name__ == "__main__":
    # do_the_work(default_settings())   # uncomment to test the LOGIC by itself
    build_ui()
