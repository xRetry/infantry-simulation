import numpy as np
import numba as nb
from typing import Optional


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


@nb.njit(nb.float32(nb.float32, nb.float32))
def calc_random_uniform(min_val: float, max_val: float) -> float:
    return (max_val - min_val) * np.random.rand() + min_val


@nb.njit(nb.float32(nb.float32, nb.float32))
def calc_delta(degree: float, distance: float):
    return np.tan(degree * 2 * np.pi / 360) * distance


@nb.njit()
def calc_recoil_numba(
        n_mag: int, x_min: float, x_max: float, y_min: float, y_max: float,
        angle_min: float, angle_max: float, fs_multi: float, x_tol: float,
        distance: float, cof_min: float, cof_max: float, cof_delta: float,
        x_comp_delay: Optional[int] = None, y_comp_delay: Optional[int] = None
):
    x = [0.]
    y = [0.]
    x_sum = 0.
    for bullet in range(1, int(n_mag)):

        x_degree: float = calc_random_uniform(x_min, x_max)
        if x_sum > x_tol:
            x_degree = -x_degree
        elif x_sum < -x_tol:
            x_degree = x_degree
        else:
            if np.random.rand() < 0.5:
                x_degree = -x_degree
        x_sum += x_degree

        y_degree = calc_random_uniform(y_min, y_max)
        if bullet == 1:
            y_degree *= fs_multi

        x_delta = calc_delta(x_degree, distance)
        y_delta = calc_delta(y_degree, distance)

        is_x_comp = x_comp_delay is not None and bullet % x_comp_delay == 0
        is_y_comp = y_comp_delay is not None and bullet % y_comp_delay == 0
        if is_y_comp:
            y_delta = 0.

        angle_deg = calc_random_uniform(angle_min, angle_max)
        angle_rad = -angle_deg * 2 * np.pi / 360

        x_rot = x_delta * np.cos(angle_rad) - y_delta * np.sin(angle_rad)
        y_rot = x_delta * np.sin(angle_rad) + y_delta * np.cos(angle_rad)

        x_new = x[bullet - 1] + x_rot
        y_new = y[bullet - 1] + y_rot

        if is_x_comp:
            x_new = x_rot
        if is_y_comp:
            y_new = y_rot

        x.append(x_new)
        y.append(y_new)

    bullets = []
    x_bloom = []
    y_bloom = []
    radius_bloom = []
    cof = cof_min
    for bullet in range(int(n_mag)):
        radius_max = np.tan(cof * np.pi / 360) * distance
        cof += cof_delta
        if cof > cof_max:
            cof = cof_max

        radius_random = np.sqrt(np.random.uniform(0, 1)) * radius_max
        angle_random = np.pi * np.random.uniform(0, 2)
        x_random = radius_random * np.cos(angle_random)
        y_random = radius_random * np.sin(angle_random)

        radius_bloom.append(radius_max)
        x_bloom.append(x[bullet] + x_random)
        y_bloom.append(y[bullet] + y_random)
        bullets.append(bullet + 1)

    return x, y, radius_bloom, x_bloom, y_bloom, bullets


if __name__ == '__main__':
    pass
