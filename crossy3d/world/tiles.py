"""
Tile geometry: boxes for grass, road, water.
"""

from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Geom, GeomTriangles, GeomNode
from panda3d.core import NodePath, Vec4

import settings


def make_box(loader, width: float, depth: float, height: float, color: Vec4):
    """Create a box: width (X), depth (Z), height (Y up). Ground is XZ."""
    format = GeomVertexFormat.get_v3n3c4()
    data = GeomVertexData("box", format, Geom.UHStatic)
    data.setNumRows(24)

    w, d, h = width / 2, depth / 2, height / 2
    # Bottom y=0, top y=h. X and Z for horizontal extent.
    verts = [
        (-w, 0, -d), (w, 0, -d), (w, 0, d), (-w, 0, d),   # bottom
        (-w, h, -d), (w, h, -d), (w, h, d), (-w, h, d),   # top
        (-w, 0, -d), (-w, h, -d), (-w, h, d), (-w, 0, d),
        (w, 0, -d), (w, h, -d), (w, h, d), (w, 0, d),
        (-w, 0, -d), (w, 0, -d), (w, h, -d), (-w, h, -d),
        (-w, 0, d), (w, 0, d), (w, h, d), (-w, h, d),
    ]
    norms = [
        (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0),
        (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),
        (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0),
        (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
        (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1),
        (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),
    ]
    tris = [
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6),
        (8, 9, 10), (8, 10, 11), (12, 14, 13), (12, 15, 14),
        (16, 17, 18), (16, 18, 19), (20, 22, 21), (20, 23, 22),
    ]
    vwriter = GeomVertexWriter(data, "vertex")
    nwriter = GeomVertexWriter(data, "normal")
    cwriter = GeomVertexWriter(data, "color")
    for i in range(24):
        vwriter.addData3(verts[i])
        nwriter.addData3(norms[i])
        cwriter.addData4(color)
    prim = GeomTriangles(Geom.UHStatic)
    for a, b, c in tris:
        prim.addVertices(a, b, c)
    geom = Geom(data)
    geom.addPrimitive(prim)
    node = GeomNode("box")
    node.addGeom(geom)
    return NodePath(node)


def create_grass_tile(loader, parent: NodePath, x: float, z: float):
    """One grass tile (green box) at world (x, z)."""
    ts = settings.TILE_SIZE
    box = make_box(loader, ts, ts, 0.1, Vec4(0.2, 0.6, 0.2, 1))
    box.reparentTo(parent)
    box.setPos(x, 0, z)
    return box


def create_road_tile(loader, parent: NodePath, x: float, z: float):
    """One road tile (dark gray)."""
    ts = settings.TILE_SIZE
    box = make_box(loader, ts, ts, 0.08, Vec4(0.25, 0.25, 0.28, 1))
    box.reparentTo(parent)
    box.setPos(x, 0, z)
    return box


def create_water_tile(loader, parent: NodePath, x: float, z: float):
    """One water tile (blue, slightly transparent look via color)."""
    ts = settings.TILE_SIZE
    box = make_box(loader, ts, ts, 0.05, Vec4(0.2, 0.4, 0.8, 1))
    box.reparentTo(parent)
    box.setPos(x, 0, z)
    return box


def create_water_lane_surface(loader, parent: NodePath, lane_z: float):
    """One continuous water surface for the whole river lane (endless water look)."""
    ts = settings.TILE_SIZE
    width = settings.LANE_WIDTH * ts
    depth = ts
    center_x = (settings.LANE_WIDTH * ts) / 2
    surface = make_box(loader, width, depth, 0.05, Vec4(0.2, 0.45, 0.85, 1))
    surface.reparentTo(parent)
    surface.setPos(center_x, 0, lane_z)
    return surface


def create_rail_tile(loader, parent: NodePath, x: float, z: float):
    """Rail / train lane (dark with rail look)."""
    ts = settings.TILE_SIZE
    box = make_box(loader, ts, ts, 0.06, Vec4(0.15, 0.15, 0.15, 1))
    box.reparentTo(parent)
    box.setPos(x, 0, z)
    return box
