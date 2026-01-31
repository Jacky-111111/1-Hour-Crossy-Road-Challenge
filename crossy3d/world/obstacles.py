"""
Bikini Bottom themed blockers: coral, palm, shell, jellyfish; buildings (Krusty Krab, Pineapple, Squidward's).
All low-poly boxes.
"""

import random
from panda3d.core import Vec4

from .tiles import make_box

import settings


# ---- Classic (kept for compatibility) ----
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


# ---- Bikini Bottom themed ----
def create_coral(loader, parent, x: float, z: float):
    """Coral: pink/red branched boxes (underwater reef style)."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("coral")
    base = make_box(loader, ts * 0.4, ts * 0.4, ts * 0.3, Vec4(0.95, 0.35, 0.4, 1))
    base.reparentTo(root)
    base.setY(ts * 0.15)
    branch1 = make_box(loader, ts * 0.15, ts * 0.15, ts * 0.5, Vec4(0.9, 0.3, 0.35, 1))
    branch1.reparentTo(root)
    branch1.setPos(ts * 0.1, ts * 0.5, 0)
    branch2 = make_box(loader, ts * 0.12, ts * 0.12, ts * 0.4, Vec4(0.85, 0.25, 0.3, 1))
    branch2.reparentTo(root)
    branch2.setPos(-ts * 0.08, ts * 0.45, ts * 0.05)
    root.setPos(x, 0, z)
    return root


def create_palm_tree(loader, parent, x: float, z: float):
    """Tropical palm: brown trunk, green fronds on top."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("palm")
    trunk = make_box(loader, ts * 0.25, ts * 0.25, ts * 0.9, Vec4(0.55, 0.35, 0.2, 1))
    trunk.reparentTo(root)
    trunk.setPos(0, ts * 0.45, 0)
    # Fronds (several green boxes)
    for i in range(4):
        frond = make_box(loader, ts * 0.4, ts * 0.1, ts * 0.15, Vec4(0.2, 0.65, 0.3, 1))
        frond.reparentTo(root)
        frond.setPos(ts * 0.15 * (1 if i < 2 else -1), ts * 1.0, ts * 0.1 * (1 if i % 2 == 0 else -1))
    top = make_box(loader, ts * 0.5, ts * 0.5, ts * 0.2, Vec4(0.15, 0.55, 0.25, 1))
    top.reparentTo(root)
    top.setPos(0, ts * 1.05, 0)
    root.setPos(x, 0, z)
    return root


def create_shell(loader, parent, x: float, z: float):
    """Sea shell: stacked curved-looking boxes (pink/cream)."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("shell")
    base = make_box(loader, ts * 0.5, ts * 0.35, ts * 0.2, Vec4(1.0, 0.85, 0.8, 1))
    base.reparentTo(root)
    base.setY(ts * 0.1)
    top = make_box(loader, ts * 0.35, ts * 0.25, ts * 0.25, Vec4(0.98, 0.8, 0.75, 1))
    top.reparentTo(root)
    top.setPos(0, ts * 0.28, ts * 0.05)
    root.setPos(x, 0, z)
    return root


def create_jellyfish(loader, parent, x: float, z: float):
    """Jellyfish: rounded body (pink/clear), thin tentacles (boxes)."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("jellyfish")
    body = make_box(loader, ts * 0.45, ts * 0.4, ts * 0.35, Vec4(1.0, 0.7, 0.9, 1))
    body.reparentTo(root)
    body.setY(ts * 0.6)
    for i in range(3):
        tent = make_box(loader, ts * 0.06, ts * 0.06, ts * 0.25, Vec4(0.9, 0.6, 0.85, 1))
        tent.reparentTo(root)
        tent.setPos(ts * (0.1 * (i - 1)), ts * 0.35, 0)
    root.setPos(x, 0, z)
    return root


def create_krusty_krab(loader, parent, x: float, z: float):
    """Krusty Krab: red building, brown roof, small sign."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("krusty_krab")
    # Main building (red)
    main = make_box(loader, ts * 0.9, ts * 0.8, ts * 0.7, Vec4(0.75, 0.2, 0.15, 1))
    main.reparentTo(root)
    main.setY(ts * 0.35)
    # Roof (brown, angled look = box on top)
    roof = make_box(loader, ts * 1.0, ts * 0.9, ts * 0.2, Vec4(0.4, 0.22, 0.12, 1))
    roof.reparentTo(root)
    roof.setY(ts * 0.75)
    # Sign (white/crustacean)
    sign = make_box(loader, ts * 0.3, ts * 0.08, ts * 0.2, Vec4(0.9, 0.85, 0.7, 1))
    sign.reparentTo(root)
    sign.setPos(0, ts * 0.85, ts * 0.35)
    root.setPos(x, 0, z)
    return root


def create_pineapple_house(loader, parent, x: float, z: float):
    """Pineapple house: yellow/orange tiered body, green leaves on top."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("pineapple_house")
    # Base (wider)
    base = make_box(loader, ts * 0.85, ts * 0.85, ts * 0.35, Vec4(0.95, 0.75, 0.2, 1))
    base.reparentTo(root)
    base.setY(ts * 0.175)
    # Middle
    mid = make_box(loader, ts * 0.7, ts * 0.7, ts * 0.4, Vec4(0.9, 0.7, 0.15, 1))
    mid.reparentTo(root)
    mid.setY(ts * 0.45)
    # Top
    top = make_box(loader, ts * 0.55, ts * 0.55, ts * 0.35, Vec4(0.85, 0.65, 0.1, 1))
    top.reparentTo(root)
    top.setY(ts * 0.725)
    # Leaves (green crown)
    for i in range(4):
        leaf = make_box(loader, ts * 0.25, ts * 0.15, ts * 0.2, Vec4(0.2, 0.6, 0.25, 1))
        leaf.reparentTo(root)
        leaf.setPos(ts * 0.15 * (1 if i < 2 else -1), ts * 0.95, ts * 0.08 * (1 if i % 2 == 0 else -1))
    crown = make_box(loader, ts * 0.4, ts * 0.4, ts * 0.15, Vec4(0.15, 0.55, 0.2, 1))
    crown.reparentTo(root)
    crown.setY(ts * 1.0)
    root.setPos(x, 0, z)
    return root


def create_squidward_house(loader, parent, x: float, z: float):
    """Squidward's house: gray/white Easter Island head style, mint trim."""
    ts = settings.TILE_SIZE
    root = parent.attachNewNode("squidward_house")
    # Main head (gray)
    main = make_box(loader, ts * 0.8, ts * 0.75, ts * 0.85, Vec4(0.6, 0.6, 0.62, 1))
    main.reparentTo(root)
    main.setY(ts * 0.425)
    # Dome top (lighter)
    dome = make_box(loader, ts * 0.6, ts * 0.55, ts * 0.3, Vec4(0.7, 0.7, 0.72, 1))
    dome.reparentTo(root)
    dome.setY(ts * 0.95)
    # Eyes (simple dark boxes)
    eye_l = make_box(loader, ts * 0.12, ts * 0.08, ts * 0.1, Vec4(0.2, 0.2, 0.25, 1))
    eye_l.reparentTo(root)
    eye_l.setPos(-ts * 0.2, ts * 0.5, ts * 0.2)
    eye_r = make_box(loader, ts * 0.12, ts * 0.08, ts * 0.1, Vec4(0.2, 0.2, 0.25, 1))
    eye_r.reparentTo(root)
    eye_r.setPos(ts * 0.2, ts * 0.5, ts * 0.2)
    # Mint trim (base)
    trim = make_box(loader, ts * 0.9, ts * 0.8, ts * 0.08, Vec4(0.5, 0.85, 0.7, 1))
    trim.reparentTo(root)
    trim.setY(ts * 0.04)
    root.setPos(x, 0, z)
    return root


def create_bikini_bottom_prop(loader, parent, x: float, z: float, kind: str = "random"):
    """Pick one Bikini Bottom themed prop. kind can be 'coral','palm','shell','jellyfish','krusty_krab','pineapple_house','squidward_house' or 'random'."""
    if kind == "random":
        # Buildings rarer than small props
        r = random.random()
        if r < 0.08:
            kind = "krusty_krab"
        elif r < 0.15:
            kind = "pineapple_house"
        elif r < 0.21:
            kind = "squidward_house"
        elif r < 0.45:
            kind = "coral"
        elif r < 0.65:
            kind = "palm_tree"
        elif r < 0.82:
            kind = "shell"
        else:
            kind = "jellyfish"
    creators = {
        "coral": create_coral,
        "palm_tree": create_palm_tree,
        "shell": create_shell,
        "jellyfish": create_jellyfish,
        "krusty_krab": create_krusty_krab,
        "pineapple_house": create_pineapple_house,
        "squidward_house": create_squidward_house,
    }
    return creators.get(kind, create_coral)(loader, parent, x, z)
