import time
from enum import Enum


def time_ms():
    return time.time_ns() // 1000000


class MovingDirection(Enum):
    LEFT = (-1, 0),
    RIGHT = (1, 0),
    UP = (0, -1),
    DOWN = (0, 1),
    IDLE = (0, 0)
