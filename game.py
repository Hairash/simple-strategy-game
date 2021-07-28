from random import randrange

from field import Field
from consts import *
from map_object import get_object_type
from player import Player


def get_neighbours(cell_x, cell_y):
    neighbours = []
    if cell_x > 0:
        neighbours.append((cell_x - 1, cell_y))
    if cell_x < N_COLS - 1:
        neighbours.append((cell_x + 1, cell_y))
    if cell_y > 0:
        neighbours.append((cell_x, cell_y - 1))
    if cell_y < N_ROWS - 1:
        neighbours.append((cell_x, cell_y + 1))
    return neighbours


class Game:
    def __init__(self, num_players, field_params, terrain_array, units, objects, buildings):
        self.num_players = num_players
        self.players = [Player(units[i], PLAYER_COLORS[i]) for i in range(self.num_players)]
        self.field = Field(*field_params)
        self.terrain_array = terrain_array
        self.objects = objects
        self.ownerless_buildings = buildings
        self.selected_cell = None
        self.selected_unit = None
        self.unit_movement_cells = None
        self.cur_player_idx = 0

    def start(self):
        self.field.draw_form()
        self.draw_field()
        self.field.main_loop(self)

    def draw_field(self):
        self.field.draw_terrain(self.terrain_array)
        self.field.draw_buildings(self.ownerless_buildings, self.players)
        self.field.draw_objects(self.objects)
        self.field.draw_units(self.players)
        if self.selected_cell:
            self.field.draw_unit_movement_cells(self.unit_movement_cells)
            self.field.select_unit(*self.selected_cell)

    def process_click(self, cell_x, cell_y):
        # print(self.cur_player_idx)
        # print(self.players[self.cur_player_idx].color)
        # print(cell_x, cell_y)
        # print(self.terrain_array[cell_x][cell_y])
        selected_unit = self.get_unit_by_cell(cell_x, cell_y)
        if selected_unit and selected_unit['player_idx'] == self.cur_player_idx and \
                not selected_unit['unit'].is_moved:
            self.select_unit(cell_x, cell_y)
        elif self.selected_cell:
            self.move_unit(cell_x, cell_y)
        else:
            selected_building = self.get_building_by_cell(cell_x, cell_y)
            if selected_building:
                building = selected_building['building']
                if get_object_type(building) == 'fortress':
                    self.create_unit(cell_x, cell_y, building.production)
        self.draw_field()

    def get_unit_by_cell(self, cell_x, cell_y):
        for player_idx in range(len(self.players)):
            player = self.players[player_idx]
            if (cell_x, cell_y) in player.units:
                return {'unit': player.units[(cell_x, cell_y)], 'player_idx': player_idx}

    def select_unit(self, cell_x, cell_y):
        if self.selected_cell == (cell_x, cell_y):
            self.selected_cell = None
            return
        self.selected_cell = (cell_x, cell_y)
        self.selected_unit = self.get_unit_by_cell(cell_x, cell_y)
        self.field.select_unit(*self.selected_cell)
        self.unit_movement_cells = self.get_unit_movement_cells()

    def move_unit(self, cell_x, cell_y):
        if (cell_x, cell_y) in self.unit_movement_cells:
            unit = self.selected_unit['unit']
            units = self.players[self.selected_unit['player_idx']].units
            del units[self.selected_cell]
            units[(cell_x, cell_y)] = unit
            unit.is_moved = True
            self.process_unit_on_cell(cell_x, cell_y)
            if self.is_end_of_turn():
                self.next_turn()
        self.selected_cell = None

    def get_unit_movement_cells(self):
        """Cells available for movement for selected unit"""
        max_step = self.selected_unit['unit'].speed
        cur_step = 0
        available_cells = [self.selected_cell]
        cur_cells = [self.selected_cell]
        while cur_step < max_step:
            next_cells = []
            for cell in cur_cells:
                for neighbour in get_neighbours(*cell):
                    # TODO: add condition - if no unit here
                    if neighbour not in available_cells and \
                            self.is_cell_passable(*neighbour):
                        next_cells.append(neighbour)
                        available_cells.append(neighbour)
            cur_cells = next_cells
            cur_step += 1
        return available_cells

    def process_unit_on_cell(self, cell_x, cell_y):
        unit = self.selected_unit['unit']
        player = self.players[self.selected_unit['player_idx']]
        map_object = self.get_object_by_cell(cell_x, cell_y)
        object_type = get_object_type(map_object)
        # TODO: bad use of string
        if object_type == 'coin':
            player.coins += map_object.value
            print('coins:', player.coins)
            del self.objects[(cell_x, cell_y)]
        building_data = self.get_building_by_cell(cell_x, cell_y)
        # TODO: very bad code
        if building_data:
            building_owner_idx = building_data['player_idx']
            building_type = get_object_type(building_data['building'])
            if building_type == 'fortress':
                if building_owner_idx != self.cur_player_idx:
                    player.buildings[(cell_x, cell_y)] = building_data['building']
                    if building_owner_idx == -1:
                        del self.ownerless_buildings[(cell_x, cell_y)]
                    else:
                        del self.players[building_owner_idx].buildings[(cell_x, cell_y)]

    def get_object_by_cell(self, cell_x, cell_y):
        if (cell_x, cell_y) in self.objects:
            return self.objects[(cell_x, cell_y)]

    def is_cell_passable(self, cell_x, cell_y):
        if self.terrain_array[cell_x][cell_y] in IMPASSABLE_TERRAIN:
            return False
        if self.get_unit_by_cell(cell_x, cell_y):
            return False
        return True

    def is_end_of_turn(self):
        units = self.players[self.cur_player_idx].units
        for unit_pos in units:
            unit = units[unit_pos]
            if not unit.is_moved:
                return False
        return True

    def next_turn(self):
        self.cur_player_idx += 1
        self.cur_player_idx %= self.num_players
        units = self.players[self.cur_player_idx].units
        for unit_pos in units:
            unit = units[unit_pos]
            unit.is_moved = False
        self.generate_objects()
        self.get_income()
        print(f'Player\'s {self.cur_player_idx} turn')
        print('Player\'s coins:', end=' ')
        for player in self.players:
            print(player.coins, end=' ')
        print()

    def generate_objects(self):
        is_new_cell_empty = False
        cell_x, cell_y = None, None
        while not is_new_cell_empty:
            cell_x = randrange(N_COLS)
            cell_y = randrange(N_ROWS)
            if self.is_ok_for_generate_new_object(cell_x, cell_y):
                is_new_cell_empty = True
        new_coin = Coin(value=randrange(3) + 1)
        self.objects[(cell_x, cell_y)] = new_coin

    def is_ok_for_generate_new_object(self, cell_x, cell_y):
        return self.is_cell_passable(cell_x, cell_y) and not self.get_object_by_cell(cell_x, cell_y)

    def get_building_by_cell(self, cell_x, cell_y):
        if (cell_x, cell_y) in self.ownerless_buildings:
            return {'building': self.ownerless_buildings[(cell_x, cell_y)], 'player_idx': -1}
        for player_idx in range(len(self.players)):
            player = self.players[player_idx]
            if (cell_x, cell_y) in player.buildings:
                return {'building': player.buildings[(cell_x, cell_y)], 'player_idx': player_idx}

    def get_income(self):
        player = self.players[self.cur_player_idx]
        for building_cell in player.buildings:
            building = player.buildings[building_cell]
            if get_object_type(building) == 'fortress':
                player.coins += building.income

    def create_unit(self, cell_x, cell_y, production):
        pass
