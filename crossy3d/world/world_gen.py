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
        self._consecutive_hazard = 0  # roads + trains
        self._consecutive_river = 0   # rivers only (can repeat so water feels continuous)
        self._last_grass_count = 0
        self._score = 0

    def set_score(self, score: int):
        self._score = score

    def _difficulty_factor(self) -> float:
        """0..1+ as score increases."""
        return min(1.5, self._score / 30.0)

    def next_lane(self, z_index: int) -> Lane:
        """Generate one lane at z_index. Ensures fair patterns. Rivers can repeat so water feels continuous."""
        df = self._difficulty_factor()
        r = random.random()

        # Force grass after too many non-river hazards (roads/trains)
        if self._consecutive_hazard >= settings.MAX_CONSECUTIVE_HAZARD:
            self._consecutive_hazard = 0
            self._consecutive_river = 0
            return self._make_grass_lane(z_index)

        # Cap consecutive rivers so we don't get endless water, but allow 2–3 for "repeated" water feel
        if self._consecutive_river >= getattr(settings, "MAX_CONSECUTIVE_RIVER", 3):
            river_chance_this_round = 0.0  # force non-river
        else:
            river_chance_this_round = settings.RIVER_LANE_CHANCE * (0.8 + 0.4 * df)

        road_chance = settings.ROAD_LANE_CHANCE * (0.8 + 0.4 * df)
        train_chance = settings.TRAIN_LANE_CHANCE * (0.5 + 0.5 * df)

        if r < train_chance:
            self._consecutive_hazard += 1
            self._consecutive_river = 0
            return TrainLane(z_index)
        r -= train_chance
        if r < road_chance:
            self._consecutive_hazard += 1
            self._consecutive_river = 0
            speed = random.uniform(
                settings.ROAD_VEHICLE_SPEED_MIN * (1 + 0.2 * df),
                settings.ROAD_VEHICLE_SPEED_MAX * (1 + 0.3 * df),
            )
            return RoadLane(z_index, random.choice([-1, 1]), speed)
        r -= road_chance
        if r < river_chance_this_round:
            self._consecutive_river += 1
            self._consecutive_hazard += 1  # river still counts as hazard for grass breaks
            speed = random.uniform(
                settings.RIVER_LOG_SPEED_MIN,
                settings.RIVER_LOG_SPEED_MAX * (1 + 0.2 * df),
            )
            return RiverLane(z_index, random.choice([-1, 1]), speed)

        self._consecutive_hazard = 0
        self._consecutive_river = 0
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
