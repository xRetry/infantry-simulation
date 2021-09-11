import math


def calc_latency(technical_latency: float, time_fly: float):
    latency = technical_latency
    if latency == -1:
        return time_fly
    return latency


def calc_refire_time(ref_time, frame_rate):
    rpm = 60 / ref_time
    rpm_dec = 1
    # decrease = 0.45062133140880894 * exp(-0.028360846520557485 * fps) + 8.559964616625598e-05 * rpm
    if frame_rate >= 0:
        a = [4.50621e-01, 2.83608466e-02, 8.55996462e-05, -2.13176645e-02]
        rpm_dec = 1 - (a[0] * math.exp(-a[1] * frame_rate) + a[2] * rpm)

    return 60 / (rpm * rpm_dec)


if __name__ == '__main__':
    pass
