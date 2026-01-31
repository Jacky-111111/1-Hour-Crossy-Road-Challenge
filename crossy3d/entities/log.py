"""
River logs: move left/right; player can stand on log (ride).
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Vec4

import settings
from world.tiles import make_box


class Log:
    """Log: stretched box, moves along X; player on top is carried."""

    def __init__(self, base: ShowBase, parent: NodePath, lane_z: float, start_x: float, length_tiles: int, direction: int, speed: float):
        self.base = base
        self.parent = parent
        self.node = parent.attachNewNode("log")
        ts = settings.TILE_SIZE
        # Raft / wooden plank (Bikini Bottom style)
        w = length_tiles * ts
        body = make_box(base.loader, w, ts * 0.5, ts * 0.25, Vec4(0.55, 0.38, 0.2, 1))
        body.reparentTo(self.node)
        self.lane_z = lane_z
        self.world_x = start_x
        self.length_tiles = length_tiles
        self.half_length = w / 2
        self.direction = direction
        self.speed = speed
        self.node.setPos(self.world_x, 0, lane_z)

    def update(self, dt: float):
        self.world_x += self.direction * self.speed * dt
        # Wrap so logs cycle in the lane – there's always a log the player can use
        ts = settings.TILE_SIZE
        lane_width = settings.LANE_WIDTH * ts
        if self.direction > 0:
            if self.world_x > lane_width + self.half_length:
                self.world_x = -self.half_length
        else:
            if self.world_x < -self.half_length:
                self.world_x = lane_width + self.half_length
        self.node.setX(self.world_x)

    def get_bounds(self):
        """(min_x, max_x, min_z, max_z) world."""
        hd = settings.TILE_SIZE * 0.4
        return (
            self.world_x - self.half_length,
            self.world_x + self.half_length,
            self.lane_z - hd,
            self.lane_z + hd,
        )

    def contains_point(self, wx: float, wz: float) -> bool:
        min_x, max_x, min_z, max_z = self.get_bounds()
        return min_x <= wx <= max_x and min_z <= wz <= max_z

    def remove(self):
        self.node.removeNode()
