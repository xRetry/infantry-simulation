from weapon import functions
from computation.iteration import iterate
from weapon.classes import Weapon


def sample_gradients(weapon_id, n_samples, n_bullets=None):
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
        wpn.cof.min,
        wpn.cof.max,
        [wpn.cof.recoil for i in range(n_samples)],
    )

    result = iterate(
        func=functions.calc_recoil,
        args=args,
        names_in=[f'in_{i}' for i in range(len(args))],
        names_out=['xy_center', 'xy'],
        flatten=False
    )

    return result


if __name__ == '__main__':
    pass
