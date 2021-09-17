from weapon import functions
from computation.iteration import iterate
from weapon.classes import Weapon


def sample_recoil(weapon_id, n_samples, x_delay=None, y_delay=None, n_bullets=None):
    wpn = Weapon(weapon_id)

    args = (
        wpn.ammo.clip_size if n_bullets is None else n_bullets,
        wpn.recoil.horizontal_min,
        wpn.recoil.horizontal_max,
        wpn.recoil.magnitude_min,
        wpn.recoil.magnitude_max,
        wpn.recoil.angle_min,
        wpn.recoil.angle_max,
        wpn.recoil.first_shot_multi,
        wpn.recoil.horizontal_tolerance,
        [10 for i in range(n_samples)],
        wpn.cof.min,
        wpn.cof.max,
        wpn.cof.recoil,
        x_delay,
        y_delay
    )

    result = iterate(
        func=functions.calc_recoil_numba,
        args=args,
        names_in=[f'in_{i}' for i in range(len(args))],
        names_out=['x_center', 'y_center', 'radius', 'x', 'y', 'bullets'],
        flatten=True
    )

    return result


if __name__ == '__main__':
    pass
