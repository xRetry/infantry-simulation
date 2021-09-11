from weapon import Weapon
from dataclasses import dataclass


@dataclass
class Health:
    base: list = (500,)
    shield_primary: list = (500,)
    shield_secondary: list = (0,)
    shield_primary_decay: list = (0,)
    shield_secondary_decay: list = (0,)


@dataclass
class Heal:
    rate: list = (0,)


@dataclass
class Resist:
    head: list = (0,)
    body: list = (0,)


@dataclass
class Skill:
    accuracy: list = (0.7, )
    headshot_ratio: list = (0.7, )
    reaction_time: list = (0,)


@dataclass
class Technical:
    latency: list = (0,)
    frame_rate: list = (0,)


class Player:  # TODO: convert to dataclass
    health: Health
    heal: Heal
    resist: Resist
    skill: Skill
    technical: Technical
    distance: tuple  # TODO: create subcategory
    weapon: Weapon

    # CONSTRUCTOR

    def __init__(self, parameter_dict=None):
        if parameter_dict is not None:
            self._load_player(parameter_dict)
        else:
            self.health = Health()
            self.heal = Heal()
            self.resist = Resist()
            self.skill = Skill()
            self.technical = Technical()
            self.distance = (0,)
            self.weapon = Weapon()

    # SETTERS

    def _load_player(self, params):
        self.health = Health(**params['health'])
        self.heal = Heal(**params['heal'])
        self.resist = Resist(**params['resist'])
        self.skill = Skill(**params['skill'])
        self.technical = Technical(**params['technical'])
        self.weapon = params['weapon']


if __name__ == '__main__':
    pl = Player()
    pass
