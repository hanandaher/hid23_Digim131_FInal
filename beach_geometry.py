import maya.cmds as cmds
import random


def create_sand(width=60, length=60, position=(0, 0, 0)):
    """Create a flat sand ground plane.

    Args:
        width    (float): Width along X.
        length   (float): Length along Z.
        position (tuple): (x, y, z) world position.

    Returns:
        str: Maya transform node name.
    """
    plane, _ = cmds.polyPlane(
        width=width,
        height=length,
        subdivisionsX=10,
        subdivisionsY=10,
        name="sand_#"
    )
    cmds.move(position[0], position[1], position[2], plane)
    return plane


def create_water(width=60, length=60, position=(0, 0.05, 10)):
    """Create an ocean water plane slightly above the sand.

    Args:
        width    (float): Width along X.
        length   (float): Length along Z.
        position (tuple): (x, y, z) world position.

    Returns:
        str: Maya transform node name.
    """
    plane, _ = cmds.polyPlane(
        width=width,
        height=length,
        subdivisionsX=20,
        subdivisionsY=20,
        name="water_#"
    )
    cmds.move(position[0], position[1], position[2], plane)
    return plane


def create_palmtree(width=1, height=10, scale=1.0, length=1, position=(0, 0, 0), axis="y"):
    """Create a palm tree: tapered cylinder trunk + radiating leaf crown.

    Args:
        width    (float): Trunk base radius multiplier.
        height   (float): Trunk height multiplier.
        scale    (float): Overall size multiplier.
        length   (float): Leaf length (passed through from config).
        position (tuple): (x, y, z) base position.
        axis     (str):   Growth axis (always y).

    Returns:
        str: Maya group node name.
    """
    px, py, pz = position
    r = max(0.1, width * scale * 0.05)  # trunk base radius
    h = max(1.0, height * scale * 0.8)  # trunk height

    parts = []

    # -- Trunk: tapered cylinder --
    trunk, _ = cmds.polyCylinder(
        radius=r,
        height=h,
        subdivisionsX=8,
        subdivisionsY=4,
        name="palm_trunk_#"
    )
    cmds.move(px, py + h * 0.5, pz, trunk)
    parts.append(trunk)

    # -- Leaf crown: 6 flat boxes fanned around the treetop --
    leaf_count = 6
    leaf_len = h * 0.65
    leaf_w = r * 3.0
    leaf_h = h * 0.05
    crown_y = py + h

    for i in range(leaf_count):
        angle = (360.0 / leaf_count) * i
        leaf, _ = cmds.polyCube(
            width=leaf_len,
            height=leaf_h,
            depth=leaf_w,
            name="palm_leaf_#"
        )
        cmds.move(px, crown_y, pz, leaf, rpr=True)
        cmds.rotate(0, angle, -30, leaf, r=True)
        cmds.move(leaf_len * 0.38, 0, 0, leaf, r=True, os=True)
        parts.append(leaf)

    group = cmds.group(parts, name="palm_tree_#")
    return group


def create_seashells(width=0.5, height=0.2, scale=1.0, position=(0, 0, 0), axis="y"):
    """Scatter cone-based seashells randomly around a centre point.

    Places between 4 and 8 shells within a patch.

    Args:
        width    (float): Scatter radius.
        height   (float): Shell cone height.
        scale    (float): Size multiplier per shell.
        position (tuple): (x, y, z) centre of the scatter patch.
        axis     (str):   Ignored — kept for API compatibility.

    Returns:
        str: Maya group node name.
    """
    px, py, pz = position
    shells = []
    count = random.randint(4, 8)

    for i in range(count):
        ox = random.uniform(-width * 3, width * 3)
        oz = random.uniform(-width * 3, width * 3)
        s = scale * random.uniform(0.6, 1.4)
        r = max(0.05, width * s * 0.5)
        h = max(0.05, height * s)

        shell, _ = cmds.polyCone(
            radius=r,
            height=h,
            subdivisionsX=8,
            name="shell_#"
        )
        tilt = random.uniform(60, 90)
        twist = random.uniform(0, 360)
        cmds.rotate(tilt, twist, 0, shell)
        cmds.move(px + ox, py, pz + oz, shell)
        shells.append(shell)

    group = cmds.group(shells, name="seashells_#")
    return group
