from weapon.functions import *
from player.functions import *
from engagement.functions import *
import utils


def time_to_kill(attacker:dict, target:dict=None, fly_time=None, trace:bool=False):
    if target is None:
        target = attacker['player_2']
        attacker = attacker['player_1']

    if fly_time is None:
        fly_time = calc_fly_time(
            distance=attacker['distance'],
            projectile_speed=attacker['weapon']['projectile']['speed']
        )

    ref_time = calc_refire_time(
        ref_time=attacker['weapon']['fire']['time_refire'],
        frame_rate=attacker['technical']['frame_rate']
    )

    dmg_body = calc_damage_body(
        dmg_max=attacker['weapon']['damage']['max'],
        dmg_min=attacker['weapon']['damage']['min'],
        range_max=attacker['weapon']['damage']['range_max'],
        range_min=attacker['weapon']['damage']['range_min'],
        distance=0
    )

    dmg_head = calc_damage_head(
        dmg_body=dmg_body,
        dmg_multi_head=attacker['weapon']['damage']['multi_head']
    )

    times, probs = calc_ttk_distribution(
        acc=attacker['skill']['accuracy'],
        hsr=attacker['skill']['headshot_ratio'],
        health_base=target['health']['base'],
        health_shield=target['health']['shield_primary'],
        health_overshield=target['health']['shield_secondary'],
        dmg_head=dmg_head,
        dmg_body=dmg_body,
        time_refire=ref_time,
        time_fly=fly_time,
        resist_head=target['resist']['head'],
        resist_body=target['resist']['body'],
        heal_rate=target['heal']['rate'],
        clip_size=attacker['weapon']['ammo']['clip_size'],
        overshield_decay=target['health']['shield_secondary_decay'],
        cutoff=0.
    )

    if trace:
        utils.trace_wrapper(attacker, 'ref_time', ref_time)
        utils.trace_wrapper(attacker, 'time_to_kill', list(times))
        utils.trace_wrapper(attacker, 'kill_probability', list(probs))

    return times, probs


def win_rate(engagement:dict, trace=False):

    players = [engagement['player_1'], engagement['player_2']]
    latency = [0, 0]
    times = [0, 0]
    probs = [0, 0]
    for pl in range(2):
        fly_time = calc_fly_time(
            distance=players[pl]['distance'],
            projectile_speed=players[pl]['weapon']['projectile']['speed']
        )

        latency[pl] = calc_latency(
            technical_latency=players[pl]['technical']['latency'],
            time_fly=fly_time
        )

        times[pl], probs[pl] = time_to_kill(players[pl], players[1-pl], fly_time, trace)

    win_rates = calc_win_rates(
        times1=times[0],
        probs1=probs[0],
        times2=times[1],
        probs2=probs[1],
        latency1=latency[0],
        latency2=latency[1]
    )
    if trace:
        utils.trace_wrapper(engagement, 'win_rates', list(win_rates))
    return win_rates


if __name__ == '__main__':
    pass
