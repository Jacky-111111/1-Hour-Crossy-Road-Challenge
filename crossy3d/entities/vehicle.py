"""
Road vehicles: moving left/right; collision kills player.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Vec4

import settings
from world.tiles import make_box


class Vehicle:
    """Car/truck: stretched box, moves along X at given speed."""

    def __init__(self, base: ShowBase, parent: NodePath, lane_z: float, grid_x: int, direction: int, speed: float):
        self.base = base
        self.parent = parent
        self.node = parent.attachNewNode("vehicle")
        ts = settings.TILE_SIZE
        # Car: longer in X (direction of travel)
        body = make_box(base.loader, ts * 1.2, ts * 0.6, ts * 0.5, Vec4(0.8, 0.2, 0.2, 1))
        body.reparentTo(self.node)
        self.node.setPos(grid_x * ts, 0, lane_z)
        self.lane_z = lane_z
        self.world_x = grid_x * ts
        self.direction = direction  # -1 or 1
        self.speed = speed
        self.half_width = ts * 0.6  # collision half-extent X
        self.half_depth = ts * 0.4  # Z

    def update(self, dt: float):
        self.world_x += self.direction * self.speed * dt
        self.node.setX(self.world_x)

    def get_bounds(self):
        """(min_x, max_x, min_z, max_z) in world."""
        hw = self.half_width
        hd = self.half_depth
        return (
            self.world_x - hw,
            self.world_x + hw,
            self.lane_z - hd,
            self.lane_z + hd,
        )

    def remove(self):
        self.node.removeNode()
