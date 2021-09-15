import numpy as np


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


def calc_random_uniform(min_val, max_val, n, random_gen=np.random.rand):
    return (max_val - min_val) * random_gen(int(n)) + min_val


def calc_sign(angles, max_angle):
    angles = angles * np.sign(np.random.rand(len(angles))-0.5)
    angle_cur = 0.
    for i in range(len(angles)):
        if angle_cur > max_angle:
            angles[i] = -abs(angles[i])
        if angle_cur < -max_angle:
            angles[i] = abs(angles[i])
        angle_cur += angles[i]
    return angles


def calc_delta(x_samples, y_samples, first_shot_multi, x_tolerance, distance):
    xy_degree = np.array([x_samples, y_samples])
    xy_degree[1, 0] *= first_shot_multi
    xy_degree[0] = calc_sign(xy_degree[0], x_tolerance)
    xy_delta = np.tan(np.deg2rad(xy_degree)) * distance
    return xy_delta


def calc_bloom_radius(min_cof, max_cof, increase, n_mag, distance):
    cof = min_cof + np.arange(0, n_mag) * increase
    cof[cof > max_cof] = max_cof
    bloom_radius = np.tan(np.deg2rad(cof)) * distance
    return bloom_radius


def calc_bloom_samples(xy, radius):
    random_radius = np.sqrt(np.random.uniform(0, 1, len(radius))) * radius
    random_angle = np.pi * np.random.uniform(0, 2, len(radius))
    xy_random = np.array([np.cos(random_angle), np.sin(random_angle)]) * random_radius
    return xy + xy_random


def calc_compensation(xy_delta, xy_compensation):
    return xy_delta - xy_delta * xy_compensation[:, None]


def calc_path(xy_delta:np.ndarray, angles:np.ndarray):
    rot_mat = np.array([
        [np.cos(np.deg2rad(angles)), -np.sin(np.deg2rad(angles))],
        [np.sin(np.deg2rad(angles)), np.cos(np.deg2rad(angles))]
    ])
    xy_rot = np.einsum('bca,ca->ba', rot_mat, xy_delta)
    xy = np.cumsum(np.hstack((np.zeros((2, 1)), xy_rot)), axis=1)
    return xy


if __name__ == '__main__':
    pass
