import itertools
import utils
from engagement.compositions import win_rate
from plotting import presets
from player.classes import Player


class Engagement:
    player_1: Player
    player_2: Player

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

    def simulate(self):
        iterator = map(
            utils.tuple_to_dict,
            zip(
                itertools.cycle('engagement'),
                zip(utils.iterate_class(self.player_1, 'player_1'), utils.iterate_class(self.player_2, 'player_2'))
            )
        )
        aggregation = {
            'player_1': dict(),
            'player_2': dict(),
        }

        for element in iterator:
            _ = win_rate(element, trace=True)
            utils.aggregate_dict(aggregation, element)

        return aggregation


if __name__ == '__main__':
    eng = Engagement(Player(), Player())
    eng.player_1.weapon.damage.max = [167]
    res = eng.simulate()
    presets.time_to_kill(res)
    pass
