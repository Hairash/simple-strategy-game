from game import Game
from unit import Unit


class TERRAIN_VALUES:
    GRASS = 'grass'
    MOUNTAIN = 'mountain'


N_COLS = 6
N_ROWS = 5
CELL_SIZE = 64
FIELD_PARAMS = (N_COLS, N_ROWS, CELL_SIZE)
# Define map
MAP = [[TERRAIN_VALUES.GRASS] * N_ROWS for _ in range(N_COLS)]
MAP[2][2], MAP[4][1] = (TERRAIN_VALUES.MOUNTAIN,) * 2
UNITS = [
    {'cell_x': 0, 'cell_y': 0, 'unit': Unit(player=0, speed=3)},
    {'cell_x': 2, 'cell_y': 1, 'unit': Unit(player=1, speed=2)},
    {'cell_x': 3, 'cell_y': 4, 'unit': Unit(player=1, speed=4)},
]


def main():
    game = Game(FIELD_PARAMS, MAP, UNITS)
    game.start()


main()
