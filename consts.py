from buildings import Fortress
from map_object import MapObject, Coin, Crystal
from unit import Unit


class TERRAIN_VALUES:
    GRASS = 'grass'
    MOUNTAIN = 'mountain'


IMPASSABLE_TERRAIN = [TERRAIN_VALUES.MOUNTAIN]

N_COLS = 6
N_ROWS = 5
CELL_SIZE = 64
FIELD_PARAMS = (N_COLS, N_ROWS, CELL_SIZE)
# Define map
MAP = [[TERRAIN_VALUES.GRASS] * N_ROWS for _ in range(N_COLS)]
MAP[2][2], MAP[4][1] = (TERRAIN_VALUES.MOUNTAIN,) * 2
UNITS = [
    {
        (0, 0): Unit(speed=3),
    },
    {
        (2, 1): Unit(speed=2),
        (3, 4): Unit(speed=4),
    },
]
OBJECTS = {
    (0, 4): Coin(value=3),
    (5, 3): Coin(value=1),
    (3, 1): Coin(value=2),
    (4, 2): Crystal(mana=5),
}

BUILDINGS = {
    (4, 4): Fortress(income=1, production={'unit': Unit(speed=1), 'cost': 5}),
    (1, 3): Fortress(income=1, production={'unit': Unit(speed=2), 'cost': 8}),
}

PLAYER_COLORS = [
    (140, 0, 0),
    (0, 0, 182),
]
