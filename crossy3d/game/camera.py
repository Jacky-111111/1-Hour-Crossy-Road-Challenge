"""
Isometric / trailing camera with smooth follow.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Quat

import settings
from utils.math3d import grid_to_world


class CameraController:
    """Smooth follow camera: above and behind player, looking forward."""

    def __init__(self, base: ShowBase):
        self.base = base
        self.camera = base.camera
        self.target_pos = Vec3(0, 0, 0)
        self.current_pos = Vec3(0, 0, 0)
        self.smoothing = settings.CAMERA_SMOOTHING
        self.distance = settings.CAMERA_DISTANCE
        self.height = settings.CAMERA_HEIGHT
        self.angle_deg = settings.CAMERA_ANGLE
        self.look_ahead = settings.CAMERA_LOOK_AHEAD
        self._shake_timer = 0.0
        self._shake_magnitude = 0.0

    def set_target_from_player(self, grid_x: int, grid_z: int):
        """Set target to follow player at (grid_x, grid_z)."""
        wx, wz = grid_to_world(grid_x, grid_z, settings.TILE_SIZE)
        # Look slightly ahead (forward = +Z)
        self.target_pos = Vec3(wx, 0, wz + self.look_ahead)

    def update(self, dt: float):
        """Smooth camera follow and optional shake."""
        # Smooth position
        self.current_pos = self.current_pos + (
            self.target_pos - self.current_pos
        ) * min(1.0, self.smoothing * dt)

        # Offset: behind and above (in camera space: -Z back, +Y up)
        import math
        rad = math.radians(self.angle_deg)
        offset_z = -self.distance * math.cos(rad)
        offset_y = self.height + self.distance * math.sin(rad)
        cam_pos = self.current_pos + Vec3(0, offset_y, offset_z)

        # Shake
        if self._shake_timer > 0:
            import random
            self._shake_timer -= dt
            s = self._shake_magnitude * (self._shake_timer / 0.3)
            cam_pos.x += (random.random() - 0.5) * 2 * s
            cam_pos.z += (random.random() - 0.5) * 2 * s

        self.camera.setPos(cam_pos)
        self.camera.lookAt(self.current_pos)

    def trigger_death_shake(self, magnitude: float = 0.4, duration: float = 0.3):
        """Brief camera jolt on death."""
        self._shake_timer = duration
        self._shake_magnitude = magnitude
