from weapon import functions
from computation.iteration import iterate
from weapon.classes import Weapon


#@nb.njit()
def calc_recoil(
        n_mag: int, x_min: float, x_max: float, y_min: float, y_max: float,
        angle_min: float, angle_max: float, fs_multi: float, x_tol: float,
        cof_min: float, cof_max: float, cof_delta: float, cof_rec_rate: float,
        cof_rec_delay: float, ref_time: float, n_burst: float, rec_pct: float, compensate: bool
):
    xy_degrees = functions.recoil_degrees(n_mag, x_min, x_max, y_min, y_max, x_tol, fs_multi)
    xy_bloom, cof_sizes, times = functions.recoil_bloom(n_mag, cof_min, cof_max, cof_delta, cof_rec_rate, cof_rec_delay, ref_time, n_burst, rec_pct)
    xy_gradients_center = functions.recoil_gradients(xy_degrees, angle_min, angle_max, compensate)
    xy_gradients = functions.recoil_gradients(xy_degrees, angle_min, angle_max, compensate, xy_bloom=xy_bloom)

    return xy_gradients_center[0], xy_gradients_center[1], xy_gradients[0], xy_gradients[1], cof_sizes, times


def sample_gradients(wpn:Weapon, n_samples, n_bullets=None, compensate=False):

    args = dict(
        n_mag=wpn.ammo.clip_size if n_bullets is None else n_bullets,
        x_min=wpn.recoil.horizontal_min,
        x_max=wpn.recoil.horizontal_max,
        y_min=wpn.recoil.magnitude_min,
        y_max=wpn.recoil.magnitude_max,
        angle_min=wpn.recoil.angle_min,
        angle_max=wpn.recoil.angle_max,
        fs_multi=wpn.recoil.first_shot_multi,
        x_tol=wpn.recoil.horizontal_tolerance,
        cof_min=wpn.cof.min,
        cof_max=wpn.cof.max,
        cof_delta=[wpn.cof.recoil for i in range(n_samples)],
        cof_rec_rate=wpn.cof.recovery_rate,
        cof_rec_delay=wpn.cof.recovery_delay,
        ref_time=wpn.fire.time_refire,
        n_burst=wpn.ammo.clip_size,  # disabled
        rec_pct=0,
        compensate=compensate
    )

    result = iterate(
        func=calc_recoil,
        args=args,
        names_out=['x_center', 'y_center', 'x', 'y', 'cof_size', 'time'],
    )

    return result


if __name__ == '__main__':
    pass
