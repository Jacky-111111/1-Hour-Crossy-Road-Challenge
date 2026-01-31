"""
Procedural lane generation: grass, road, river, train with difficulty scaling.
"""

import random
from typing import List, Optional

import settings
from .lane import Lane, LaneType, GrassLane, RoadLane, RiverLane, TrainLane


class WorldGenerator:
    """Generate lanes forward; guarantee safe progression."""

    def __init__(self):
        self._consecutive_hazard = 0
        self._last_grass_count = 0
        self._score = 0

    def set_score(self, score: int):
        self._score = score

    def _difficulty_factor(self) -> float:
        """0..1+ as score increases."""
        return min(1.5, self._score / 30.0)

    def next_lane(self, z_index: int) -> Lane:
        """Generate one lane at z_index. Ensures fair patterns."""
        df = self._difficulty_factor()
        r = random.random()

        # Force grass after too many hazards
        if self._consecutive_hazard >= settings.MAX_CONSECUTIVE_HAZARD:
            self._consecutive_hazard = 0
            return self._make_grass_lane(z_index)

        # Lane type chances (scaled by difficulty)
        road_chance = settings.ROAD_LANE_CHANCE * (0.8 + 0.4 * df)
        river_chance = settings.RIVER_LANE_CHANCE * (0.8 + 0.4 * df)
        train_chance = settings.TRAIN_LANE_CHANCE * (0.5 + 0.5 * df)

        if r < train_chance:
            self._consecutive_hazard += 1
            return TrainLane(z_index)
        r -= train_chance
        if r < road_chance:
            self._consecutive_hazard += 1
            speed = random.uniform(
                settings.ROAD_VEHICLE_SPEED_MIN * (1 + 0.2 * df),
                settings.ROAD_VEHICLE_SPEED_MAX * (1 + 0.3 * df),
            )
            return RoadLane(z_index, random.choice([-1, 1]), speed)
        r -= road_chance
        if r < river_chance:
            self._consecutive_hazard += 1
            speed = random.uniform(
                settings.RIVER_LOG_SPEED_MIN,
                settings.RIVER_LOG_SPEED_MAX * (1 + 0.2 * df),
            )
            return RiverLane(z_index, random.choice([-1, 1]), speed)

        self._consecutive_hazard = 0
        return self._make_grass_lane(z_index)

    def _make_grass_lane(self, z_index: int) -> GrassLane:
        lane = GrassLane(z_index)
        chance = settings.GRASS_BLOCKER_CHANCE
        cluster = settings.GRASS_BLOCKER_CLUSTER
        for x in range(settings.LANE_WIDTH):
            if random.random() < chance:
                lane.add_blocker(x)
                if random.random() < cluster and x + 1 < settings.LANE_WIDTH:
                    lane.add_blocker(x + 1)
        return lane
