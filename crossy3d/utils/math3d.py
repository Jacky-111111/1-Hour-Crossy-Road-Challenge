"""
3D math helpers for grid and world.
"""


def grid_to_world(x: int, z: int, tile_size: float = 1.0) -> tuple:
    """Convert grid (lane_x, lane_z) to world (x, z) center of tile."""
    return (x * tile_size, z * tile_size)


def world_to_grid(x: float, z: float, tile_size: float = 1.0) -> tuple:
    """Convert world position to grid indices."""
    import math
    gx = int(math.floor(x / tile_size + 0.5))
    gz = int(math.floor(z / tile_size + 0.5))
    return (gx, gz)


def clamp(value, min_val, max_val):
    """Clamp value to [min_val, max_val]."""
    return max(min_val, min(max_val, value))
