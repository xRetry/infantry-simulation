from weapon import functions
from computation.graph import Graph, Input, Operation
from weapon.classes import Weapon
import numpy as np


def built_recoil():
    angle_min = Input(0)
    angle_max = Input(1)
    n_mag = Input(2)
    distance = Input(3)
    x_min = Input(4)
    x_max = Input(5)
    y_min = Input(6)
    y_max = Input(7)
    fs_multi = Input(8)
    x_tol = Input(9)
    cof_min = Input(10)
    cof_max = Input(11)
    cof_increase = Input(12)
    xy_compensation = Input(13)

    n_mag_minus = Operation(lambda x: x-1, args=(n_mag,))
    angles = Operation(functions.calc_random_uniform, args=(angle_min, angle_max, n_mag_minus))
    x_samples = Operation(functions.calc_random_uniform, args=(x_min, x_max, n_mag_minus))
    y_samples = Operation(functions.calc_random_uniform, args=(y_min, y_max, n_mag_minus))
    xy_delta = Operation(functions.calc_delta, args=(x_samples, y_samples, fs_multi, x_tol, distance))

    xy_comp = Operation(functions.calc_compensation, args=(xy_delta, xy_compensation))

    xy = Operation(functions.calc_path, args=(xy_comp, angles), name='xy')
    bloom_radius = Operation(functions.calc_bloom_radius, args=(cof_min, cof_max, cof_increase, n_mag, distance), name='radius')
    xy_true = Operation(functions.calc_bloom_samples, args=(xy, bloom_radius), name='xy_true')
    return Graph(xy_true)


def sample_recoil(weapon_id, n_samples):
    recoil_graph = built_recoil()

    wpn = Weapon(weapon_id)

    result = recoil_graph(
        wpn.recoil.angle_min,
        wpn.recoil.angle_max,
        wpn.ammo.clip_size,
        [10 for i in range(n_samples)],
        wpn.recoil.magnitude_min,
        wpn.recoil.magnitude_max,
        wpn.recoil.horizontal_min,
        wpn.recoil.horizontal_max,
        wpn.recoil.first_shot_multi,
        wpn.recoil.horizontal_tolerance,
        wpn.cof.min,
        wpn.cof.max,
        wpn.cof.recoil,
        [np.array([0, 1])]
    )
    return result


if __name__ == '__main__':
    pass
