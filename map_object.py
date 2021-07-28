def get_object_type(map_object):
    return type(map_object).__name__.lower()


class MapObject:
    pass
    # def __init__(self, params):
    #     pass
    #     self.type = object_type
    #     self.params = params


class Coin(MapObject):
    def __init__(self, value):
        # super().__init__(value)
        self.value = value


class Crystal(MapObject):
    def __init__(self, mana):
        # super().__init__(mana)
        self.mana = mana
