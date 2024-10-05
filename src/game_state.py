from enum import Enum


class Estado(Enum):
    NOT_STARTED = 0
    NOT_ENOUGH = 1
    GAME_RUNNING = 2
    END_GAME = 3
