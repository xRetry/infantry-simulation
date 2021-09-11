import numba
import math


@numba.njit()
def calc_ttk_distribution(
        acc: float,
        hsr: float,
        health_base: float,
        health_shield: float,
        health_overshield: float,
        dmg_head: float,
        dmg_body: float,
        time_refire: float,
        time_fly: float,
        resist_head: float,
        resist_body: float,
        heal_rate: float,
        clip_size: int,
        overshield_decay: float,
        cutoff: float = 0.
):
    # Compute full initial health pool
    health_init: numba.float32 = health_base + health_shield + health_overshield
    # Set up probabilities for events
    probs_step = [
        1 - acc,  # miss
        acc * (1 - hsr),  # body hit
        acc * hsr  # head hit
    ]
    # Set up damages for events
    dmg_vals = [
        0,  # miss
        dmg_body,  # body hit
        dmg_head  # head hit
    ]
    # Set up damage resistance values for events
    resist_vals = [
        0,
        resist_body,
        resist_head
    ]
    # Set up health and probability storage
    time_to_kills = numba.typed.List.empty_list(item_type=numba.types.float64)
    ttk_probs = numba.typed.List.empty_list(item_type=numba.types.float64)
    healths = numba.typed.Dict.empty(key_type=numba.types.float64, value_type=numba.types.float64)
    # Set up initial values
    healths[health_init] = 1.
    time: numba.float32 = time_fly
    # Iterate through all shots
    for s in range(clip_size):
        ttk_probs.append(0.)  # TODO: create full list beforehand
        time_to_kills.append(time)
        healths_new = numba.typed.Dict.empty(key_type=numba.types.float64, value_type=numba.types.float64)
        # Iterate through all health values
        for health, prob in healths.items():
            # Iterate through all events
            for j in range(3):
                # Reset health and probability
                h_cur = health
                p_cur = prob
                # Subtract overshield decay
                if h_cur > health_init - health_overshield:
                    h_cur -= overshield_decay * time_refire
                    # Make sure reduced health doesn't exceed overshield
                    if h_cur < health_init - health_overshield:
                        h_cur = health_init - health_overshield
                # Calc new health value and probability
                h_cur = h_cur - dmg_vals[j] * (1-resist_vals[j])
                p_cur = p_cur * probs_step[j]
                # Save probability and time if target dead
                if h_cur <= 0:
                    ttk_probs[s] += p_cur
                    continue
                # Skip if probability below cutoff
                if p_cur < cutoff:
                    continue
                # Add healing
                if h_cur < health_base:
                    h_cur += heal_rate * time_refire
                    if h_cur > health_base:
                        h_cur = health_base
                # Get old probability for current health
                p_old = healths_new.get(h_cur)
                # Check if entry for new health value already exits
                if p_old is None:
                    p_old = 0.
                # Combine old and new probabilities of health values
                healths_new[h_cur] = p_cur + p_old
        # Increase time
        time += time_refire
        # Update health storage
        healths = healths_new

    # Sum up remaining probabilities for non-kills
    p_nokill = 0.
    for p in healths.values():
        p_nokill += p
    ttk_probs.append(p_nokill)
    time_to_kills.append(math.inf)
    return time_to_kills, ttk_probs


@numba.njit()
def calc_win_rates(times1, probs1, times2, probs2, latency1, latency2):
    win_probs = numba.typed.List([0., 0., 0.])
    for i in range(len(times1)):
        sums = numba.typed.List([0., 0., 0.])
        for j in range(len(times2)):
            if times2[j] > times1[i] + latency2:
                sums[1] += probs2[j]
            elif times2[j] < times1[i] - latency1:
                sums[2] += probs2[j]
            else:
                sums[0] += probs2[j]
        for j in range(3):
            win_probs[j] += probs1[i] * sums[j]
    return win_probs



if __name__ == '__main__':
    pass