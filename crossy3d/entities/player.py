"""
Player: grid position, hop animation, collision, ride-on-log.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, NodePath, Vec4

import settings
from utils.math3d import grid_to_world
from utils.easing import ease_in_out_quad, hop_height, squash_stretch
from game.input import DIRECTIONS


class Player:
    """One tile per hop; smooth hop animation; no diagonals."""

    def __init__(self, base: ShowBase, parent: NodePath):
        self.base = base
        self.parent = parent
        self.node = parent.attachNewNode("player")
        self._build_visual(base.loader)
        self.grid_x = 0
        self.grid_z = 0
        self.world_x = 0.0
        self.world_z = 0.0
        self._hop_start_x = 0.0
        self._hop_start_z = 0.0
        self._hop_end_x = 0.0
        self._hop_end_z = 0.0
        self._hop_t = 1.0  # 1 = not hopping
        self._hop_duration = settings.PLAYER_HOP_DURATION
        self._hop_height = settings.PLAYER_HOP_HEIGHT
        self._squash = settings.PLAYER_SQUASH_SCALE
        self.riding_log = None  # NodePath or None when on a log
        self.alive = True

    def _build_visual(self, loader):
        """SpongeBob-style character: yellow sponge body, brown shorts, big eyes, smile."""
        from world.tiles import make_box
        from panda3d.core import Vec4
        ts = settings.TILE_SIZE
        # Sponge body (slightly rectangular, bright yellow)
        body = make_box(loader, ts * 0.55, ts * 0.5, ts * 0.5, Vec4(1.0, 0.95, 0.3, 1))
        body.reparentTo(self.node)
        body.setY(ts * 0.25)
        # Brown shorts / pants at bottom
        pants = make_box(loader, ts * 0.5, ts * 0.45, ts * 0.18, Vec4(0.45, 0.25, 0.1, 1))
        pants.reparentTo(self.node)
        pants.setY(ts * 0.09)
        # Left eye (white + blue pupil)
        eye_l = make_box(loader, ts * 0.12, ts * 0.08, ts * 0.14, Vec4(1, 1, 1, 1))
        eye_l.reparentTo(self.node)
        eye_l.setPos(-ts * 0.12, ts * 0.55, ts * 0.08)
        pupil_l = make_box(loader, ts * 0.06, ts * 0.04, ts * 0.06, Vec4(0.2, 0.5, 0.9, 1))
        pupil_l.reparentTo(self.node)
        pupil_l.setPos(-ts * 0.12, ts * 0.62, ts * 0.08)
        # Right eye
        eye_r = make_box(loader, ts * 0.12, ts * 0.08, ts * 0.14, Vec4(1, 1, 1, 1))
        eye_r.reparentTo(self.node)
        eye_r.setPos(ts * 0.12, ts * 0.55, ts * 0.08)
        pupil_r = make_box(loader, ts * 0.06, ts * 0.04, ts * 0.06, Vec4(0.2, 0.5, 0.9, 1))
        pupil_r.reparentTo(self.node)
        pupil_r.setPos(ts * 0.12, ts * 0.62, ts * 0.08)
        # Smile (wide pink mouth)
        mouth = make_box(loader, ts * 0.25, ts * 0.04, ts * 0.06, Vec4(1.0, 0.4, 0.5, 1))
        mouth.reparentTo(self.node)
        mouth.setPos(0, ts * 0.42, -ts * 0.05)
        self.node.setPos(0, 0, 0)

    def get_grid_pos(self):
        return (self.grid_x, self.grid_z)

    def is_hopping(self) -> bool:
        return self._hop_t < 1.0

    def can_accept_input(self) -> bool:
        """Accept new move (either idle or buffer during hop)."""
        return True

    def try_move(self, direction: str, is_blocked: callable) -> bool:
        """Attempt move in direction. Returns True if move started."""
        if self.is_hopping():
            return False
        dx, dz = DIRECTIONS.get(direction, (0, 0))
        if dx == 0 and dz == 0:
            return False
        nx = self.grid_x + dx
        nz = self.grid_z + dz
        if is_blocked(nx, nz):
            return False
        self._start_hop(nx, nz)
        return True

    def _start_hop(self, end_x: int, end_z: int):
        self._hop_start_x = self.world_x
        self._hop_start_z = self.world_z
        self._hop_end_x, self._hop_end_z = grid_to_world(end_x, end_z, settings.TILE_SIZE)
        self._hop_t = 0.0
        self.grid_x = end_x
        self.grid_z = end_z

    def update(self, dt: float):
        """Advance hop animation; apply ride-on-log offset."""
        if self._hop_t < 1.0:
            self._hop_t = min(1.0, self._hop_t + dt / self._hop_duration)
            t = ease_in_out_quad(self._hop_t)
            self.world_x = self._hop_start_x + (self._hop_end_x - self._hop_start_x) * t
            self.world_z = self._hop_start_z + (self._hop_end_z - self._hop_start_z) * t
            h = hop_height(self._hop_t, self._hop_height)
            squash = squash_stretch(self._hop_t, self._squash)
            self.node.setPos(self.world_x, h, self.world_z)  # Y-up: hop arc
            self.node.setScale(squash)
            if self._hop_t >= 1.0:
                self.node.setScale(1.0)
                self.world_x = self._hop_end_x
                self.world_z = self._hop_end_z
        else:
            self.node.setPos(self.world_x, 0, self.world_z)
        if self.riding_log:
            # Offset from log is applied by game (player world pos = log pos + offset)
            pass

    def set_position_from_log(self, log_world_x: float, log_world_z: float, offset_x: float, offset_z: float):
        """When on log: world position = log + offset (in tile units)."""
        ts = settings.TILE_SIZE
        self.world_x = log_world_x + offset_x * ts
        self.world_z = log_world_z + offset_z * ts
        self.node.setPos(self.world_x, 0, self.world_z)

    def get_world_pos(self):
        return (self.world_x, self.world_z)

    def kill(self):
        self.alive = False

    def reset(self, grid_x: int = 0, grid_z: int = 0):
        self.grid_x = grid_x
        self.grid_z = grid_z
        self.world_x, self.world_z = grid_to_world(grid_x, grid_z, settings.TILE_SIZE)
        self._hop_t = 1.0
        self.riding_log = None
        self.alive = True
        self.node.setPos(self.world_x, 0, self.world_z)
        self.node.setScale(1.0)
