from unit import Unit


class Building:
    pass


class Fortress(Building):
    def __init__(self, income, production: dict):
        self.income = income
        self.production = production


class Cellar(Building):
    def __init__(self, coins):
        self.coins = coins
