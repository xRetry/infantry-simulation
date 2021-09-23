import numpy as np
import numba as nb
from scipy import optimize
from typing import Optional, Iterable


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


@nb.njit()
def in_ellipse(x_el, y_el, a, b, x, y):
    v = (x - x_el)**2 / a**2 + (y - y_el)**2 / b**2
    return v <= 1


def accuracy_from_hits(is_hit: np.ndarray, aggregator:callable) -> float:
    accs = is_hit.sum(axis=1) / len(is_hit[0])
    return aggregator(accs)


@nb.njit()
def obj_aim_point(xy_center:np.ndarray, x, y, a, b):
    is_in = ((x - xy_center[0]) ** 2 / a ** 2 + (y - xy_center[1]) ** 2 / b ** 2) <= 1
    accs = is_in.sum(axis=1) / len(is_in[0])
    return 1-accs.mean()


def fit_target(x: np.ndarray, y: np.ndarray, distance: np.ndarray, per_bullet=False):
    n_bullets = len(x[0, :])
    bullets = [n_bullets]
    if per_bullet:
        bullets = np.arange(1, n_bullets+1, dtype=np.int32)
    accs = np.zeros((len(bullets), len(distance)))
    centers = np.zeros((len(bullets), len(distance), 2))
    for b in range(len(bullets)):
        for d in range(len(distance)):
            x_dis = x[:, :bullets[b]] * distance[d]
            y_dis = y[:, :bullets[b]] * distance[d]
            sol = optimize.minimize(
                obj_aim_point,
                np.array([x_dis.mean(), y_dis.mean()]),
                args=(x_dis, y_dis, 0.0950435176, 0.0950435176),
                method='Nelder-Mead'
            )
            accs[b, d] = 1 - sol.fun
            centers[b, d, :] = sol.x
    return centers, accs


def accuracy_to_dps(accs, distances, wpn):
    dps = np.zeros_like(accs)
    for d in range(len(distances)):
        dmg = calc_damage_body(
            dmg_min=wpn.damage.min,
            dmg_max=wpn.damage.max,
            range_min=wpn.damage.range_min,
            range_max=wpn.damage.range_max,
            distance=distances[d]
        )
        n_bul = len(accs[:, d])
        cof = (np.arange(n_bul) + 1) * wpn.cof.recoil
        cof[(cof + wpn.cof.min) > wpn.cof.max] = wpn.cof.max - wpn.cof.min
        rec_time = cof / wpn.cof.recovery_rate + wpn.cof.recovery_delay
        fire_time = (np.arange(n_bul) + 1) * wpn.fire.time_refire
        dmgs = (np.arange(n_bul) + 1) * dmg
        dps[:, d] = dmgs / (fire_time + rec_time) * accs[:, d]

    return dps


@nb.njit(nb.float32(nb.float32, nb.float32))
def uniform_random(min_val: float, max_val: float) -> float:
    return (max_val - min_val) * np.random.rand() + min_val


@nb.njit()
def recoil_degrees(n_mag: int, x_min: float, x_max: float, y_min: float, y_max: float, x_tol: float, fs_multi: float):
    xy_degrees = np.zeros((2, int(n_mag)), dtype=np.float32)
    x_sum = 0.
    for bullet in range(1, int(n_mag)):

        x_degree = uniform_random(x_min, x_max)
        if x_sum > x_tol:
            x_degree = -x_degree
        elif x_sum < -x_tol:
            x_degree = x_degree
        else:
            if np.random.rand() < 0.5:
                x_degree = -x_degree
        x_sum += x_degree

        y_degree = uniform_random(y_min, y_max)
        if bullet == 1:
            y_degree *= fs_multi

        xy_degrees[0, bullet] = x_degree
        xy_degrees[1, bullet] = y_degree
    return xy_degrees


@nb.njit()
def recoil_gradients(xy_degrees, angle_min, angle_max, compensate=False, xy_bloom=None):
    xy_gradients = np.zeros_like(xy_degrees)
    for bullet in range(0, len(xy_degrees[0, :])):
        angle_deg = uniform_random(angle_min, angle_max)
        angle_rad = np.deg2rad(-angle_deg)

        xy = xy_degrees[:, bullet]
        if compensate:
            xy[1] = 0

        if xy_bloom is not None:
            xy[0] += xy_bloom[0, bullet]
            xy[1] += xy_bloom[1, bullet]

        xy_grad_vert = np.tan(np.deg2rad(xy))

        x_rot = xy_grad_vert[0] * np.cos(angle_rad) - xy_grad_vert[1] * np.sin(angle_rad)
        y_rot = xy_grad_vert[0] * np.sin(angle_rad) + xy_grad_vert[1] * np.cos(angle_rad)

        if compensate:
            xy_gradients[0, bullet] = x_rot
            xy_gradients[1, bullet] = y_rot
        else:
            xy_gradients[0, bullet] = xy_gradients[0, bullet-1] + x_rot
            xy_gradients[1, bullet] = xy_gradients[1, bullet-1] + y_rot

    return xy_gradients


@nb.njit()
def recoil_bloom(n_mag, cof_min, cof_max, cof_delta, cof_rec_rate, cof_rec_delay, ref_time, n_burst, rec_pct):
    n_mag = int(n_mag)
    xy_bloom = np.zeros((2, n_mag), dtype=np.float32)
    cof_sizes = np.zeros(n_mag, dtype=np.float32)
    times = np.zeros(n_mag, dtype=np.float32)

    cof = cof_min
    time = 0.
    n_burst_cur = 1
    for bullet in range(n_mag):
        cof += cof_delta
        if cof > cof_max:
            cof = cof_max

        times[bullet] = time
        time += ref_time
        if n_burst_cur == n_burst:
            n_burst_cur = 0
            if rec_pct > 0:
                cof_dec = (cof - cof_min) * rec_pct
                time += (cof_dec/cof_rec_rate) + cof_rec_delay
                cof = cof-cof_dec
        n_burst_cur += 1
        cof_sizes[bullet] = cof

        radius_random = np.sqrt(np.random.uniform(0, 1)) * cof
        angle_random = np.pi * np.random.uniform(0, 2)
        x_random = radius_random * np.cos(angle_random)
        y_random = radius_random * np.sin(angle_random)
        xy_bloom[0, bullet] = x_random
        xy_bloom[1, bullet] = y_random

    return xy_bloom, cof_sizes, times


if __name__ == '__main__':
    pass
