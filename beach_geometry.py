"""
beach_geometry.py
=======================================
Digim 131 | Author: Hanan
Geometry builders for the beach scene.

create_sand(width, height, position)       -- sand ground plane
create_water(width, height, position)      -- ocean water plane
create_palmtree(width, height, scale, length, position) -- trunk OR leaves
create_seashells(width, height, scale, position)        -- a seashell
"""

import maya.cmds as cmds


def create_sand(width=60, height=60, position=(0, 0, 0)):
    """Create the sand ground plane.

    Args:
        width (float): size along X
        height (float): size along Z
        position (tuple): (x, y, z) placement

    Returns:
        str: name of the created plane
    """
    plane = cmds.polyPlane(w=width, h=height, sx=10, sy=10, name="sand_#")[0]
    cmds.move(position[0], position[1], position[2], plane)
    return plane


def create_water(width=60, height=60, position=(0, 0.1, 0)):
    """Create the ocean water plane, slightly above the sand.

    Args:
        width (float): size along X
        height (float): size along Z
        position (tuple): (x, y, z) placement

    Returns:
        str: name of the created plane
    """
    plane = cmds.polyPlane(w=width, h=height, sx=20, sy=20, name="water_#")[0]
    cmds.move(position[0], position[1], position[2], plane)
    return plane


def create_palmtree(width=1, height=10, scale=1, length=1, position=(0, 0, 0)):
    """Create one part of a palm tree (trunk OR leaves, based on shape).

    A tall, thin cylinder makes the trunk. A short, wide cylinder
    makes a leaf cluster. Use two config entries (trunk + leaves)
    to build a full tree.

    Args:
        width (float): radius of the cylinder
        height (float): height of the cylinder
        scale (float): overall scale multiplier
        length (float): unused, kept for config compatibility
        position (tuple): (x, y, z) placement

    Returns:
        str: name of the created cylinder
    """
    part = cmds.polyCylinder(
        r=width * 0.05 * scale,
        h=height * 0.1 * scale,
        sx=8,
        name="palm_#"
    )[0]
    cmds.move(position[0], position[1], position[2], part)
    return part


def create_seashells(width=0.5, height=0.2, scale=1, position=(0, 0, 0)):
    """Create a single seashell using a cone shape.

    Args:
        width (float): radius of the cone
        height (float): height of the cone
        scale (float): overall scale multiplier
        position (tuple): (x, y, z) placement

    Returns:
        str: name of the created cone
    """
    shell = cmds.polyCone(
        r=width * scale,
        h=height * scale,
        sx=8,
        name="seashell_#"
    )[0]
    cmds.move(position[0], position[1], position[2], shell)
    return shell