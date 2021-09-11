import numpy as np

DIR = 'C:\\Users\\Marco\\Dropbox\\Privat\\Coding Projects\\Python\\engagement_simulation\\'

# Player colors for plotting
PLAYER_COLORS = ['royalblue', 'firebrick', 'grey']

# Colors for plotting sample results
SAMPLE_COLORS = ['tab:orange', 'tab:green', 'tab:pink', 'tab:olive', 'tab:cyan', 'tab:purple']

#
WEAPON_MAPPING = {
    'name': ['full', 'name'],
    'projectile': {
        'speed': ['fire_mode', 'projectile_speed_override'],
        'speed_max': ['fire_mode', 'projectile', 'speed_max'],
        'acceleration': ['fire_mode', 'projectile', 'acceleration'],
        'lifespan': ['fire_mode', 'projectile', 'lifespan'],
        'drag': ['fire_mode', 'projectile', 'drag'],
        'gravity': ['fire_mode', 'projectile', 'gravity']
    },
    'damage': {
        'max': ['fire_mode', 'max_damage'],
        'min': ['fire_mode', 'min_damage'],
        'range_max': ['fire_mode', 'max_damage_range'],
        'range_min': ['fire_mode', 'min_damage_range'],
        'multi_head': ['fire_mode', 'damage_head_multiplier'],
        'multi_legs': ['fire_mode', 'damage_legs_multiplier'],
        'shield_bypass_pct': ['fire_mode', 'shield_bypass_pct']
    },
    'recoil': {
        'angle_max': ['fire_mode', 'recoil_angle_max'],
        'angle_min': ['fire_mode', 'recoil_angle_min'],
        'first_shot_multi': ['fire_mode', 'recoil_first_shot_modifier'],
        'horizontal_max': ['fire_mode', 'recoil_horizontal_max'],
        'horizontal_min': ['fire_mode', 'recoil_horizontal_min'],
        'horizontal_tolerance': ['fire_mode', 'recoil_horizontal_tolerance'],
        'increase': ['fire_mode', 'recoil_increase'],
        'increase_crouched': ['fire_mode', 'recoil_increase_crouched'],
        'magnitude_max': ['fire_mode', 'recoil_magnitude_max'],
        'magnitude_min': ['fire_mode', 'recoil_magnitude_min'],
        'magnitude_total_max': ['fire_mode', 'recoil_max_total_magnitude'],
        'magnitude_shots_at_min': ['fire_mode', 'recoil_shots_at_min_magnitude'],
        'recovery_acceleration': ['fire_mode', 'recoil_recovery_acceleration'],
        'recovery_delay': ['fire_mode', 'recoil_recovery_delay_ms'],
        'recovery_rate': ['fire_mode', 'recoil_recovery_rate']
    },
    'reload': {
        'ammo_fill': ['fire_mode', 'reload_ammo_fill_ms'],
        'chamber': ['fire_mode', 'reload_chamber_ms'],
        'time': ['fire_mode', 'reload_time_ms']
    },
    'cof': {
        'min': ['player_state', 'cof_min'],
        'max': ['player_state', 'cof_max'],
        'grow_rate': ['player_state', 'cof_grow_rate'],
        'recovery_delay': ['player_state', 'cof_recovery_delay_ms'],
        'recovery_rate': ['player_state', 'cof_recovery_rate'],
        'recovery_delay_threshold': ['player_state', 'cof_recovery_delay_threshold'],
        'turn_penalty': ['player_state', 'cof_turn_penalty'],
        'pellet_spread': ['fire_mode', 'cof_pellet_spread'],
        'range': ['fire_mode', 'cof_range'],
        'recoil': ['fire_mode', 'cof_recoil'],
        'scalar': ['fire_mode', 'cof_scalar'],
        'scalar_moving': ['fire_mode', 'cof_scalar_moving']
    },
    'fire': {
        'ammo_per_shot': ['fire_mode', "fire_ammo_per_shot"],
        'time_auto_fire': ['fire_mode', "fire_auto_fire_ms"],
        'burst_count': ['fire_mode', "fire_burst_count"],
        'time_charge_up': ['fire_mode', "fire_charge_up_ms"],
        'time_delay': ['fire_mode', "fire_delay_ms"],
        'detect_range': ['fire_mode', "fire_detect_range"],
        'time_refire': ['fire_mode', "fire_refire_ms"],
        'pellets_per_shot': ['fire_mode', "fire_pellets_per_shot"]
    },
    'ammo': {
        'clip_size': ['full', 'ammo', 'clip_size'],
        'capacity': ['full', 'ammo', 'capacity'],
        'reload_speed': ['full', 'ammo', 'reload_ms']
    }
}

# Details for attachments modifiers
ATT_MODIFIERS = {
    ('damage', 'range_max'): {
        'var': 'FireGroup.ProjectileDamageFallOffStart',
        'operation': np.sum
    },
    ('damage', 'range_min'): {
        'var': 'FireGroup.ProjectileDamageFallOffEnd',
        'operation': np.sum
    },
    ('projectile', 'speed'): {
        'var': 'FireGroup.ProjectileSpeedMultiplier',
        'operation': np.prod
    },
    ('cof', 'scalar_moving'): {
        'var': 'FireMode.CofScalarMoving',
        'operation': np.prod
    },
    ('recoil', 'magnitude'): {
        'var': 'FireMode.RecoilMagnitudeModifier',
        'operation': np.prod
    },
    ('fire', 'detect_range'): {
        'var': 'FireMode.FireDetectRange',
        'operation': np.sum
    }
}