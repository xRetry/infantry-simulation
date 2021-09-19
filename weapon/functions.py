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


@nb.njit()
def calc_degrees(n_mag: int, x_min: float, x_max: float, y_min: float, y_max: float, x_tol: float, fs_multi: float):
    xy_degrees = np.zeros((2, int(n_mag)), dtype=np.float32)
    x_sum = 0.
    for bullet in range(1, int(n_mag)):

        x_degree = calc_random_uniform(x_min, x_max)
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

        xy_degrees[0, bullet] = xy_degrees[0, bullet - 1] + x_degree
        xy_degrees[1, bullet] = xy_degrees[1, bullet - 1] + y_degree
    return xy_degrees


@nb.njit()
def calc_gradients(xy_degrees, angle_min, angle_max):
    xy_gradients = np.zeros_like(xy_degrees)
    for bullet in range(len(xy_degrees[0, :])):
        angle_deg = calc_random_uniform(angle_min, angle_max)
        angle_rad = np.deg2rad(-angle_deg)

        xy_grad_vert = np.tan(np.deg2rad(xy_degrees[:, bullet]))

        xy_gradients[0, bullet] = xy_grad_vert[0] * np.cos(angle_rad) - xy_grad_vert[1] * np.sin(angle_rad)
        xy_gradients[1, bullet] = xy_grad_vert[0] * np.sin(angle_rad) + xy_grad_vert[1] * np.cos(angle_rad)
    return xy_gradients


@nb.njit()
def calc_bloom(xy_degrees, cof_min, cof_max, cof_delta):
    xy_bloom = np.zeros_like(xy_degrees)
    cof = cof_min
    for bullet in range(len(xy_degrees[0, :])):
        cof += cof_delta
        if cof > cof_max:
            cof = cof_max

        radius_random = np.sqrt(np.random.uniform(0, 1)) * cof
        angle_random = np.pi * np.random.uniform(0, 2)
        x_random = radius_random * np.cos(angle_random)
        y_random = radius_random * np.sin(angle_random)

        xy_bloom[0, bullet] = xy_degrees[0, bullet] + x_random
        xy_bloom[1, bullet] = xy_degrees[1, bullet] + y_random

    return xy_bloom


#@nb.njit()
def calc_recoil(
        n_mag: int, x_min: float, x_max: float, y_min: float, y_max: float,
        angle_min: float, angle_max: float, fs_multi: float, x_tol: float,
        cof_min: float, cof_max: float, cof_delta: float
):
    xy_degrees = calc_degrees(n_mag, x_min, x_max, y_min, y_max, x_tol, fs_multi)
    xy_bloom = calc_bloom(xy_degrees, cof_min, cof_max, cof_delta)
    xy_gradients_center = calc_gradients(xy_degrees, angle_min, angle_max)
    xy_gradients = calc_gradients(xy_bloom, angle_min, angle_max)
    return xy_gradients_center, xy_gradients


if __name__ == '__main__':
    pass
