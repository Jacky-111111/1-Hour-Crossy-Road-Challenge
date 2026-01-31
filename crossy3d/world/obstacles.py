"""
Blockers: trees (trunk + leaves), rocks. Low-poly boxes.
"""

from panda3d.core import Vec4

from .tiles import make_box

import settings


def create_tree(loader, parent, x: float, z: float):
    """Tree: box trunk + box leaves. Y-up. Returns root NodePath."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("tree")
    trunk = make_box(loader, ts * 0.3, ts * 0.3, ts * 0.8, Vec4(0.4, 0.25, 0.1, 1))
    trunk.reparentTo(root)
    trunk.setPos(0, ts * 0.4, 0)
    leaves = make_box(loader, ts * 0.9, ts * 0.9, ts * 0.9, Vec4(0.15, 0.5, 0.2, 1))
    leaves.reparentTo(root)
    leaves.setPos(0, ts * 1.1, 0)
    root.setPos(x, 0, z)
    return root


def create_rock(loader, parent, x: float, z: float):
    """Rock: small box. Y-up."""
    ts = settings.TILE_SIZE
    rock = make_box(loader, ts * 0.6, ts * 0.6, ts * 0.4, Vec4(0.35, 0.35, 0.38, 1))
    rock.reparentTo(parent)
    rock.setPos(x, 0, z)
    return rock
