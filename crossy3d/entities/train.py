"""
Train: fast, long; warning then kill on contact.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Vec4

import settings
from world.tiles import make_box


class Train:
    """Train: long row of boxes; moves at high speed after warning."""

    def __init__(self, base: ShowBase, parent: NodePath, lane_z: float, direction: int):
        self.base = base
        self.parent = parent
        self.node = parent.attachNewNode("train")
        ts = settings.TILE_SIZE
        length = settings.TRAIN_LENGTH
        for i in range(length):
            seg = make_box(base.loader, ts * 0.9, ts * 0.6, ts * 0.8, Vec4(0.2, 0.2, 0.2, 1))
            seg.reparentTo(self.node)
            seg.setX(i * ts - (length - 1) * ts / 2)
        self.lane_z = lane_z
        self.length = length
        self.half_length = (length * ts) / 2
        self.direction = direction
        self.speed = settings.TRAIN_SPEED
        self.world_x = -self.half_length - 5 if direction > 0 else self.half_length + 5
        self.active = False  # starts moving after warning
        self.warning_timer = settings.TRAIN_WARNING_TIME
        self.node.setPos(self.world_x, 0, lane_z)

    def update(self, dt: float):
        if self.warning_timer > 0:
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                self.active = True
            return
        if self.active:
            self.world_x += self.direction * self.speed * dt
            self.node.setX(self.world_x)

    def get_bounds(self):
        hd = settings.TILE_SIZE * 0.4
        return (
            self.world_x - self.half_length,
            self.world_x + self.half_length,
            self.lane_z - hd,
            self.lane_z + hd,
        )

    def is_active(self) -> bool:
        return self.active

    def is_warning(self) -> bool:
        return self.warning_timer > 0

    def remove(self):
        self.node.removeNode()
