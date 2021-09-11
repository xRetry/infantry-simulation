

def calc_damage_body(dmg_max: float, dmg_min: float, range_max: float, range_min: float, distance: float) -> float:
    if distance <= range_max:  # in max damage range
        dmg_body = dmg_max
    elif distance >= range_min:  # in min damage range
        dmg_body = dmg_min
    else:  # in linear region
        slope = (dmg_max - dmg_min) / (range_max - range_min)
        dmg_body = dmg_max + slope * (distance - range_max)
    return dmg_body


def calc_damage_head(dmg_body: float, dmg_multi_head: float) -> float:
    dmg_head = dmg_body * dmg_multi_head
    return dmg_head


def calc_fly_time(distance: float, projectile_speed: float) -> float:
    """
    Returns the travel time of a bullet to the target.

    :param distance: The distance to the target [m]
    :param projectile_speed: Velocity of the bullet [m/s]
    :return: Travel time to target [s]
    """
    return 1 / projectile_speed * distance


if __name__ == '__main__':
    pass
