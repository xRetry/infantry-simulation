import ps2.weapon_loader
from typing import List
from dataclasses import dataclass


@dataclass
class Damage:
    max: list = (143, )
    min: list = (112, )
    range_max: list = (10, )
    range_min: list = (65, )
    multi_head: list = (2, )
    multi_legs: list = (0.5, )
    shield_bypass_pct: list = (0, )


@dataclass
class Fire:
    ammo_per_shot: list = (30, )
    time_auto_fire: list = (0, )
    burst_count: list = (1, )
    time_charge_up: list = (0, )
    time_delay: list = (0, )
    detect_range: list = (25, )
    time_refire: list = (0.01, )
    pellets_per_shot: list = (1, )


@dataclass
class Recoil:
    angle_max: list = (0, )
    angle_min: list = (0, )
    first_shot_multi: list = (0, )
    horizontal_max: list = (0, )
    horizontal_min: list = (0, )
    horizontal_tolerance: list = (0, )
    increase: list = (0, )
    increase_crouched: list = (0, )
    magnitude_max: list = (0, )
    magnitude_min: list = (0, )
    magnitude_total_max: list = (0, )
    magnitude_shots_at_min: list = (0, )
    recovery_acceleration: list = (0, )
    recovery_delay: list = (0, )
    recovery_rate: list = (0, )


@dataclass
class Projectile:
    speed: list = (500, )
    speed_max: list = (0, )
    acceleration: list = (0, )
    lifespan: list = (1.5, )
    drag: list = (0, )
    gravity: list = (9.81, )


@dataclass
class Reload:
    ammo_fill: list = (2, )
    chamber: list = (2, )
    time: list = (2, )


@dataclass
class Cof:
    min: list = (0, )
    max: list = (0, )
    grow_rate: list = (0, )
    recovery_delay: list = (0, )
    recovery_rate:list = (0, )
    recovery_delay_threshold: list = (0, )
    turn_penalty: list = (0, )
    pellet_spread: list = (0, )
    range: list = (0, )
    recoil: list = (0, )
    scalar: list = (0, )
    scalar_moving: list = (0, )

@dataclass
class Ammo:
    clip_size: list = (30, )
    capacity: list = (120, )
    reload_speed: list = (3, )


@dataclass
class Weapon:
    # VARIABLES
    name: str
    damage: Damage
    fire: Fire
    recoil: Recoil
    cof: Cof
    reload: Reload
    projectile: Projectile
    ammo: Ammo

    # CONSTRUCTOR

    def __init__(self, weapon_id=None, attachments:List[str]=()):
        # Load weapon and modifications
        if weapon_id is not None:
            self._load_weapon(weapon_id, attachments)
        else:
            self.name = 'default'
            self.damage = Damage()
            self.fire = Fire()
            self.recoil = Recoil()
            self.cof = Cof()
            self.reload = Reload()
            self.projectile = Projectile()
            self.ammo = Ammo()

    # SETTERS

    def _load_weapon(self, weapon_id:int, attachments:List[str]=()):
        # Load and format stats file
        stats = ps2.weapon_loader.extract_stats(weapon_id, attachments=attachments)
        # Assign variables
        self.damage = Damage(**stats['damage'])
        self.fire = Fire(**stats['fire'])
        self.cof = Cof(**stats['cof'])
        self.reload = Reload(**stats['reload'])
        self.recoil = Recoil(**stats['recoil'])
        self.projectile = Projectile(**stats['projectile'])
        self.ammo = Ammo(**stats['ammo'])


if __name__ == '__main__':
    pass


