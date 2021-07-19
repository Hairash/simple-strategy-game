import pygame


WHITE = (255, 255, 255)
GRAY = (150, 150, 150)


def get_terrain_images(cell_size):
    # class TERRAIN_VALUES:
    #     GRASS = pygame.transform.scale(pygame.image.load('images/grass.png'), (cell_size, cell_size)),
    #
    # return TERRAIN_VALUES()
    # from main import TERRAIN_VALUES
    return {
        # TODO: make it better
        # TERRAIN_VALUES.GRASS: pygame.transform.scale(pygame.image.load('images/grass.png'), (cell_size, cell_size)),
        'grass': pygame.transform.scale(pygame.image.load('images/grass.png'), (cell_size, cell_size)),
        'mountain': pygame.transform.scale(pygame.image.load('images/mountain.png'), (cell_size, cell_size)),
    }


def get_unit_images(cell_size):
    return {
        0: pygame.transform.scale(pygame.image.load('images/unit red.png'), (cell_size, cell_size)),
        1: pygame.transform.scale(pygame.image.load('images/unit blue.png'), (cell_size, cell_size)),
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

    def draw_form(self):
        width = self.n_cols * self.cell_size
        height = self.n_rows * self.cell_size
        print(width, height)
        pygame.init()
        pygame.display.set_caption("Simple strategy")
        self.window = pygame.display.set_mode((width, height))
        self.window.fill(GRAY)

    def draw_terrain(self, terrain_array):
        for cell_x in range(len(terrain_array)):
            for cell_y in range(len(terrain_array[cell_x])):
                x, y = self.cell_image_coordinates(cell_x, cell_y)
                self.window.blit(self.TERRAIN_IMAGES[terrain_array[cell_x][cell_y]], (x, y))

    def cell_image_coordinates(self, cell_x, cell_y):
        x = self.cell_size * cell_x
        y = self.cell_size * cell_y
        return x, y

    def main_loop(self):
        while not self.is_game_ended:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_ended = True
            pygame.display.update()

    def draw_units(self, unit_array):
        for unit_cell in unit_array:
            x, y = self.cell_image_coordinates(unit_cell['cell_x'], unit_cell['cell_y'])
            self.window.blit(self.UNIT_IMAGES[unit_cell['unit'].player], (x, y))
