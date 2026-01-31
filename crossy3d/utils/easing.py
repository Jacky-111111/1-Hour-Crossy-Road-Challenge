"""
Easing functions for smooth hop and camera animations.
"""

import math


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease in-out. t in [0, 1]."""
    if t < 0.5:
        return 2 * t * t
    return 1 - pow(-2 * t + 2, 2) / 2


def ease_out_quad(t: float) -> float:
    """Quadratic ease out."""
    return 1 - (1 - t) * (1 - t)


def ease_in_quad(t: float) -> float:
    """Quadratic ease in."""
    return t * t


def hop_height(t: float, peak_height: float) -> float:
    """Parabolic hop: 0 at t=0 and t=1, peak at t=0.5."""
    if t <= 0 or t >= 1:
        return 0.0
    return 4 * peak_height * t * (1 - t)


def squash_stretch(t: float, squash: float) -> float:
    """Scale: slight squash at land (t=1). Returns scale factor."""
    if t >= 1:
        return squash
    # Slight stretch during hop
    return 1.0 + (1.0 - squash) * 0.2 * math.sin(t * math.pi)
