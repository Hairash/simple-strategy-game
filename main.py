from consts import *
from game import Game


def main():
    game = Game(2, FIELD_PARAMS, MAP, UNITS, OBJECTS, BUILDINGS)
    game.start()


main()
