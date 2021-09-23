import numpy as np

import ps2.weapon_loader
from typing import Collection, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

import weapon.functions


@dataclass
class Damage:
    max: Collection or float = 143
    min: Collection or float = 112
    range_max: Collection or float = 10
    range_min: Collection or float = 65
    multi_head: Collection or float = 2
    multi_legs: Collection or float = 0.5
    shield_bypass_pct: Collection or float = 0


@dataclass
class Fire:
    ammo_per_shot: Collection or float = 30
    time_auto_fire: Collection or float = 0
    burst_count: Collection or float = 1
    time_charge_up: Collection or float = 0
    time_delay: Collection or float = 0
    detect_range: Collection or float = 25
    time_refire: Collection or float = 0.01
    pellets_per_shot: Collection or float = 1


@dataclass
class Recoil:
    angle_max: Collection or float = 0
    angle_min: Collection or float = 0
    first_shot_multi: Collection or float = 0
    horizontal_max: Collection or float = 0
    horizontal_min: Collection or float = 0
    horizontal_tolerance: Collection or float = 0
    increase: Collection or float = 0
    increase_crouched: Collection or float = 0
    magnitude_max: Collection or float = 0
    magnitude_min: Collection or float = 0
    magnitude_total_max: Collection or float = 0
    magnitude_shots_at_min: Collection or float = 0
    recovery_acceleration: Collection or float = 0
    recovery_delay: Collection or float = 0
    recovery_rate: Collection or float = 0


@dataclass
class Projectile:
    speed: Collection or float = 600
    speed_max: Collection or float = 0
    acceleration: Collection or float = 0
    lifespan: Collection or float = 1.5
    drag: Collection or float = 0
    gravity: Collection or float = 9.81


@dataclass
class Reload:
    ammo_fill: Collection or float = 2
    chamber: Collection or float = 2
    time: Collection or float = 2


@dataclass
class Cof:
    min: Collection or float = 0
    max: Collection or float = 0
    grow_rate: Collection or float = 0
    recovery_delay: Collection or float = 0
    recovery_rate:Collection or float = 0
    recovery_delay_threshold: Collection or float = 0
    turn_penalty: Collection or float = 0
    pellet_spread: Collection or float = 0
    range: Collection or float = 0
    recoil: Collection or float = 0
    scalar: Collection or float = 0
    scalar_moving: Collection or float = 0


@dataclass
class Ammo:
    clip_size: Collection or float = 30
    capacity: Collection or float = 120
    reload_speed: Collection or float = 3


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

    def __init__(self, weapon_id:Optional[int]=None, attachments:Collection[str]=()):
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

    def _load_weapon(self, weapon_id:int, attachments:Collection[str]=()):
        # Load and format stats file
        stats = ps2.weapon_loader.extract_stats(weapon_id, attachments=attachments)
        # Assign variables
        self.name = stats['name']
        self.damage = Damage(**stats['damage'])
        self.fire = Fire(**stats['fire'])
        self.cof = Cof(**stats['cof'])
        self.reload = Reload(**stats['reload'])
        self.recoil = Recoil(**stats['recoil'])
        self.projectile = Projectile(**stats['projectile'])
        self.ammo = Ammo(**stats['ammo'])


class Hitbox(ABC):

    @abstractmethod
    def check_hits(self, x, y) -> np.ndarray:
        pass

    @abstractmethod
    def accuracy(self, x, y) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class EllipseHitbox(Hitbox):
    _name: str
    x_center: float
    y_center: float
    x_size: float
    y_size: float

    def __init__(self, name, x_center, y_center, x_size, y_size):
        self._name = name
        self.x_center = x_center
        self.y_center = y_center
        self.x_size = x_size
        self.y_size = y_size

    def check_hits(self, x, y) -> np.ndarray:
        return weapon.functions.in_ellipse(
            self.x_center,
            self.y_center,
            self.x_size,
            self.y_size,
            x,
            y
        )

    def accuracy(self, x, y) -> float:
        is_hit = self.check_hits(x, y)
        return weapon.functions.accuracy_from_hits(is_hit, np.mean)

    @property
    def name(self) -> str:
        return self._name


if __name__ == '__main__':
    pass


