import pygame
from consts import *
from map_object import get_object_type

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
ORANGE = (255, 200, 0)

INDENT = 2
BORDER_WIDTH = 3


def get_terrain_images(cell_size):
    # class TERRAIN_VALUES:
    #     GRASS = pygame.transform.scale(pygame.image.load('images/grass.png'), (cell_size, cell_size)),
    #
    # return TERRAIN_VALUES()
    # from main import TERRAIN_VALUES
    return {
        TERRAIN_VALUES.GRASS: pygame.transform.scale(pygame.image.load('images/grass.png'), (cell_size, cell_size)),
        TERRAIN_VALUES.MOUNTAIN: pygame.transform.scale(pygame.image.load('images/mountain.png'), (cell_size, cell_size)),
    }


def get_unit_images(cell_size):
    return {
        # -1: pygame.transform.scale(pygame.image.load('images/selection.png'), (cell_size, cell_size)),
        0: pygame.transform.scale(pygame.image.load('images/unit red.png'), (cell_size, cell_size)),
        1: pygame.transform.scale(pygame.image.load('images/unit blue.png'), (cell_size, cell_size)),
    }


def get_object_images(cell_size):
    return {
        'coin': pygame.transform.scale(pygame.image.load('images/coin.png'), (cell_size, cell_size)),
        'crystal': pygame.transform.scale(pygame.image.load('images/crystal.png'), (cell_size, cell_size)),
    }


def get_building_images(cell_size):
    return {
        'fortress': pygame.transform.scale(pygame.image.load('images/fortress.png'), (cell_size, cell_size)),
        'cellar': pygame.transform.scale(pygame.image.load('images/cellar.png'), (cell_size, cell_size)),
    }


class Field:
    def __init__(self, n_cols, n_rows, cell_size):
        self.is_game_ended = False
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.cell_size = cell_size
        self.window = None  # initializing below
        self.TERRAIN_IMAGES = get_terrain_images(self.cell_size)
        self.UNIT_IMAGES = get_unit_images(self.cell_size)
        self.OBJECT_IMAGES = get_object_images(self.cell_size)
        self.BUILDING_IMAGES = get_building_images(self.cell_size)

    def draw_form(self):
        width = self.n_cols * self.cell_size
        height = self.n_rows * self.cell_size
        print(width, height)
        pygame.init()
        pygame.display.set_caption("Simple strategy")
        self.window = pygame.display.set_mode((width, height))

    def draw_terrain(self, terrain_array):
        self.window.fill(GRAY)
        for cell_x in range(len(terrain_array)):
            for cell_y in range(len(terrain_array[cell_x])):
                x, y = self.cell_image_coordinates(cell_x, cell_y)
                self.window.blit(self.TERRAIN_IMAGES[terrain_array[cell_x][cell_y]], (x, y))

    def cell_image_coordinates(self, cell_x, cell_y):
        x = self.cell_size * cell_x
        y = self.cell_size * cell_y
        return x, y

    def main_loop(self, game):
        while not self.is_game_ended:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_ended = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cell_x, cell_y = self.get_cur_cell()
                        game.process_click(cell_x, cell_y)
            pygame.display.update()

    def draw_units(self, players):
        for player_idx in range(len(players)):
            player = players[player_idx]
            for cell in player.units:
                x, y = self.cell_image_coordinates(*cell)
                self.window.blit(self.UNIT_IMAGES[player_idx], (x, y))

    def get_cur_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        cur_cell = self.coordinates_to_cell(*mouse_pos)
        return cur_cell

    def coordinates_to_cell(self, x, y):
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        return cell_x, cell_y

    def select_unit(self, cell_x, cell_y):
        x, y = self.cell_image_coordinates(cell_x, cell_y)
        pygame.draw.rect(
            self.window, YELLOW,
            (x + INDENT, y + INDENT, self.cell_size - INDENT * 2, self.cell_size - INDENT * 2),
            BORDER_WIDTH + 1
        )

    def draw_cell(self, cell_x, cell_y, terrain, unit=None):
        x, y = self.cell_image_coordinates(cell_x, cell_y)
        pygame.draw.rect(self.window, GRAY, (x, y, self.cell_size, self.cell_size))
        self.window.blit(self.TERRAIN_IMAGES[terrain], (x, y))
        if unit:
            self.window.blit(self.UNIT_IMAGES[unit.player], (x, y))

    def draw_unit_movement_cells(self, unit_movement_cells):
        for cell in unit_movement_cells:
            x, y = self.cell_image_coordinates(cell[0], cell[1])
            pygame.draw.rect(
                self.window, ORANGE,
                (x + INDENT, y + INDENT, self.cell_size - INDENT * 2, self.cell_size - INDENT * 2),
                BORDER_WIDTH
            )

    def draw_objects(self, objects):
        for object_cell in objects:
            x, y = self.cell_image_coordinates(*object_cell)
            map_object = objects[object_cell]
            object_type = get_object_type(map_object)
            self.window.blit(self.OBJECT_IMAGES[object_type], (x, y))

    def draw_buildings(self, ownerless_buildings, players):
        for building_cell in ownerless_buildings:
            x, y = self.cell_image_coordinates(*building_cell)
            building = ownerless_buildings[building_cell]
            # TODO: rename to get_type_string and move to constants
            building_type = get_object_type(building)
            self.window.blit(self.BUILDING_IMAGES[building_type], (x, y))
        for player in players:
            for building_cell in player.buildings:
                # TODO: repeat - draw_building
                x, y = self.cell_image_coordinates(*building_cell)
                building = player.buildings[building_cell]
                building_type = get_object_type(building)
                self.window.blit(self.BUILDING_IMAGES[building_type], (x, y))
                # TODO: repeat - draw_cell_border
                pygame.draw.rect(
                    self.window, player.color,
                    (x + INDENT * 2, y + INDENT * 2, self.cell_size - INDENT * 2 * 2, self.cell_size - INDENT * 2 * 2),
                    BORDER_WIDTH
                )
