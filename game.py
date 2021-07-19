from field import Field


class Game:
    def __init__(self, field_params, terrain_array, units):
        self.field = Field(*field_params)
        self.terrain_array = terrain_array
        self.units = units

    def start(self):
        self.field.draw_form()
        self.field.draw_terrain(self.terrain_array)
        self.field.draw_units(self.units)
        self.field.main_loop()
