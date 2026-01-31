"""
Lane types: Grass, Road, River, Train.
"""

from abc import ABC, abstractmethod
from typing import Set, List, Optional, Any
import random

import settings


class LaneType:
    GRASS = "grass"
    ROAD = "road"
    RIVER = "river"
    TRAIN = "train"


class Lane(ABC):
    """Base lane: has type, z index, and optional blockers / entities."""

    def __init__(self, z_index: int):
        self.z_index = z_index
        self.blocked_tiles: Set[tuple] = set()  # (x, z) blocked for movement
        self.safe_tiles: Set[tuple] = set()     # (x,) or (x, z) that are safe
        self._lane_width = settings.LANE_WIDTH

    @abstractmethod
    def get_type(self) -> str:
        pass

    def is_blocked(self, grid_x: int) -> bool:
        """Is (grid_x, self.z_index) blocked for movement?"""
        return (grid_x, self.z_index) in self.blocked_tiles

    def is_safe_tile(self, grid_x: int) -> bool:
        """Override in subclasses (e.g. road: never safe, river: on log)."""
        return (grid_x, self.z_index) not in self.blocked_tiles


class GrassLane(Lane):
    """Safe lane; may have trees/rocks as blockers."""

    def get_type(self) -> str:
        return LaneType.GRASS

    def add_blocker(self, grid_x: int):
        self.blocked_tiles.add((grid_x, self.z_index))


class RoadLane(Lane):
    """Cars move left/right; direction and speeds; gaps are "safe" only when no car there."""

    def get_type(self) -> str:
        return LaneType.ROAD

    def __init__(self, z_index: int, direction: int, speed: float):
        super().__init__(z_index)
        self.direction = direction  # -1 left, 1 right
        self.speed = speed
        # Vehicle positions (grid_x) are updated in world; we don't store them here for logic
        # Collision is done in world by checking player vs vehicle bounds


class RiverLane(Lane):
    """Logs move; safe only when standing on a log."""

    def get_type(self) -> str:
        return LaneType.RIVER

    def __init__(self, z_index: int, direction: int, speed: float):
        super().__init__(z_index)
        self.direction = direction
        self.speed = speed
        # Log segments: list of (start_x, length) in grid; movement handled in world


class TrainLane(Lane):
    """Rare; warning then fast train."""

    def get_type(self) -> str:
        return LaneType.TRAIN

    def __init__(self, z_index: int):
        super().__init__(z_index)
        self.warning_time = settings.TRAIN_WARNING_TIME
        self.speed = settings.TRAIN_SPEED
        self.length = settings.TRAIN_LENGTH
