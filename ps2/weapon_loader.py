import ps2.utils
import constants
from typing import List


def weapon_from_api(id_or_name:int or str) -> dict:
    """
    Requests weapon stats from Planeside 2 Census API.

    :param id_or_name: item_id or full weapon name
    :return: Unformated dictionary of stats
    """
    if isinstance(id_or_name, str):
        query_var = 'name.en'
    else:
        query_var = 'item_id'
    query = f'http://census.daybreakgames.com/get/ps2/item?{query_var}={id_or_name}&c:lang=en&c:join=fire_mode^inject_at:fire_mode^list:1,item_to_weapon^inject_at:fire_mode_2(weapon,weapon_to_fire_group^on:weapon_id^to:weapon_id^list:1(fire_group^on:fire_group_id^to:fire_group_id,fire_group_to_fire_mode^on:fire_group_id^to:fire_group_id^list:1(fire_mode_2^on:fire_mode_id^to:fire_mode_id^list:1(player_state_group^list:1^inject_at:player_state_group,player_state_group_2^on:player_state_group_id^to:player_state_group_id^inject_at:player_state_group_2^list:1,fire_mode_to_projectile^on:fire_mode_id^to:fire_mode_id^inject_at:projectile(projectile^on:projectile_id^to:projectile_id^inject_at:projectile_details))))))&c:join=weapon_datasheet^inject_at:ammo&c:join=item_category^on:item_category_id^to:item_category_id^inject_at:category&c:join=item_attachment^on:item_id^to:item_id^list:1^inject_at:attachments(item^on:attachment_item_id^to:item_id^inject_at:attachment(zone_effect^on:passive_ability_id^to:ability_id^inject_at:attachment_effects^list:1(zone_effect_type^on:zone_effect_type_id^to:zone_effect_type_id^inject_at:attachment_effects_description)))'

    data = ps2.utils.query_from_api(query)
    return data


def format_weapon(raw:dict) -> dict:
    """
    Formats raw weapon data into a more readable structure. Removes some stats.

    :param raw: Dictionary of unformated weapon data
    :return: Better structured stats dictionary
    """
    # Load player states
    player_states = ps2.utils.json_to_dict('player_state')['player_state_list']

    # Add high-level data
    weapon_keys = ['name', 'item_id', 'item_type_id', 'faction_id', 'category']
    data = {}
    for key in weapon_keys:
        val = raw['item_list'][0][key]
        if isinstance(val, dict):
            if key == 'category':
                name = val.pop('name')
                val['name'] = name['en']
            if 'en' in val.keys():
                key = 'name'
                val = val['en']
        else:
            val = float(val)
        data[key] = val

    # Add ammo stats
    data['ammo'] = {}
    ammo_stats = raw['item_list'][0]['ammo']
    ammo_keys = ['reload_ms', 'clip_size', 'capacity']
    for key in ammo_keys:
        data['ammo'][key] = float(ammo_stats[key])

    # Add change and recover times
    for key, val in raw['item_list'][0]['fire_mode_2']['weapon_id_join_weapon'].items():
        data[key] = float(val)

    # Iterate through fire groups
    fire_groups = raw['item_list'][0]['fire_mode_2']['weapon_id_join_weapon_to_fire_group']
    fire_modes_list = []
    for fire_group in fire_groups:
        # Iterate through fire modes
        fire_modes = fire_group['fire_group_id_join_fire_group_to_fire_mode']
        for fire_mode in fire_modes:
            # Iterate through weapon stats
            stats = fire_mode['fire_mode_id_join_fire_mode_2'][0]
            fire_mode_stats = {}
            for key, val in stats.items():
                if key == 'description':
                    fire_mode_stats['name'] = val['en']
                # Value is list (skip player state for now)
                elif isinstance(val, list):
                    continue
                # Value is dictionary (only for key=projectile)
                elif isinstance(val, dict):
                    val = val['projectile_details)']
                    for k, v in val.items():
                        val[k] = float(v)
                    fire_mode_stats[key] = val
                # Value is numeric
                else:
                    fire_mode_stats[key] = float(val)
            # Add player states
            player_state_list = format_player_state(stats, player_states)
            fire_mode_stats['player_state'] = player_state_list
            fire_modes_list.append(fire_mode_stats)
    data['fire_mode'] = fire_modes_list

    # Add attachments
    att_list = format_attachments(raw['item_list'][0]['attachments'])
    data['attachments'] = att_list
    return data


def format_player_state(stats:dict, player_states:list) -> list:
    """
    Subfunction to format raw weapon data. Restructures player state stats (= players stances).

    :param stats: Dictionary of all player state stats of a weapon
    :param player_states: Helper list which contains all player states with dictionaries of name and id
    :return: Restructured list of player state stats
    """
    state_list = []
    for player_state in player_states:
        new = {}
        # Add name of state
        new['name'] = player_state['description']
        # Add main stats of stance
        for stance in stats['player_state_group_2']:
            if player_state['player_state_id'] == stance['player_state_id']:
                for k, v in stance.items():
                    new[k] = float(v)
        # Add additional stat of stance
        for stance in stats['player_state_group']:
            if player_state['description'] == stance['player_state']:
                new['min_cone_of_fire'] = float(stance['min_cone_of_fire'])
        state_list.append(new)
    return state_list


def format_attachments(data:list):
    """
    Subfunction to format raw weapon data. Restructures attachment stats of a weapon.

    :param data: List of all available attachments of a weapon
    :return: Restructured list of available weapon attachments
    """
    att_list = []
    for entry in data:
        entry = entry['attachment']
        if 'attachment_effects' not in entry.keys():
            continue
        new_att = {
            'name': entry['name']['en'],
            'item_id': entry['item_id']
        }
        effects = []
        for eff in entry['attachment_effects']:
            new_eff = {}
            for key, desc in eff['attachment_effects_description'].items():
                if key == 'description':
                    new_eff['name'] = desc
                    continue
                if key in eff.keys():
                    try:
                        new_eff[desc] = float(eff[key])
                    except ValueError:
                        new_eff[desc] = eff[key]
            effects.append(new_eff)
        new_att['effect'] = effects
        att_list.append(new_att)
    return att_list


def save_weapon(data:dict):
    """
    Saves provided weapon data as .json to specific subfolder.

    :param data: Dictionary of weapon data
    :return: None
    """
    file_name = str(int(data['item_id']))
    path = constants.DIR + '\\resources\\weapons\\'
    ps2.utils.dict_to_json(data, file_name, path)


def download_weapon(id_or_name):
    """
    Requests, formats and stores data for a specific weapon.

    :param id_or_name: item_id or full name of a weapon
    :return: None
    """
    raw_data = weapon_from_api(id_or_name)
    formatted_data = format_weapon(raw_data)
    save_weapon(formatted_data)


def extract_stats(item_id:int, player_state_id:int=0, fire_mode:str='Auto', ads:bool=True, attachments:List[str]=()) -> dict:
    """
    Loads relevant weapon data for engagement simulator from preformatted weapon data file.

    :param item_id: ID of weapon to load stats for
    :param player_state_id: Wanted player state (stance), 0=Standing
    :param fire_mode: Wanted fire mode (Auto/Semi-Auto/Burst?) TODO: check burst name
    :param ads: Aiming down sight or hip-fire
    :param attachments: List of attachment (full name required)
    :return: Formatted weapon data for engagement simulation
    """
    data = {}
    # Load stats file of weapon

    data['full'] = ps2.utils.json_to_dict(str(item_id), constants.DIR + 'resources\\weapons\\')
    # Filter data by fire mode
    data_fire_modes = ps2.utils.filter_list(data['full']['fire_mode'], name=fire_mode)
    # Filter ADS/hip-fire
    fire_mode_type_id = 0
    if ads:
        fire_mode_type_id = 1
    data['fire_mode'] = ps2.utils.filter_list(data_fire_modes, fire_mode_type_id=fire_mode_type_id)[0]
    # Filter player state (stance)
    data['player_state'] = ps2.utils.filter_list(data['fire_mode']['player_state'], player_state_id=player_state_id)[0]

    # Sanity check
    if data['player_state']['cof_min'] != data['player_state']['min_cone_of_fire']:
        raise ValueError('Difference of min cof!')

    # Adding values to stats dict
    '''
    stats = {
        'name': data_full['name'],
        'projectile': {
            'speed': data_fire_mode['projectile_speed_override'],
            'speed_max': data_fire_mode['projectile']['speed_max'],
            'acceleration': data_fire_mode['projectile']['acceleration'],
            'lifespan': data_fire_mode['projectile']['lifespan'],
            'drag': data_fire_mode['projectile']['drag'],
            'gravity': data_fire_mode['projectile']['gravity']
        },
        'damage': {
            'max': data_fire_mode['max_damage'],
            'min': data_fire_mode['min_damage'],
            'range_max': data_fire_mode['max_damage_range'],
            'range_min': data_fire_mode['min_damage_range'],
            'multi_head': data_fire_mode['damage_head_multiplier'],
            'multi_legs': data_fire_mode['damage_legs_multiplier'],
            'shield_bypass_pct': data_fire_mode['shield_bypass_pct']
        },
        'recoil': {
            'angle_max': data_fire_mode['recoil_angle_max'],
            'angle_min': data_fire_mode['recoil_angle_min'],
            'first_shot_multi': data_fire_mode['recoil_first_shot_modifier'],
            'horizontal_max': data_fire_mode['recoil_horizontal_max'],
            'horizontal_min': data_fire_mode['recoil_horizontal_min'],
            'horizontal_tolerance': data_fire_mode['recoil_horizontal_tolerance'],
            'increase': data_fire_mode['recoil_increase_crouched'] if player_state_id == (1 or 5) else data_fire_mode['recoil_increase'],
            'magnitude_max': data_fire_mode['recoil_magnitude_max'],
            'magnitude_min': data_fire_mode['recoil_magnitude_min'],
            'magnitude_total_max': data_fire_mode['recoil_max_total_magnitude'],
            'magnitude_shots_at_min': data_fire_mode['recoil_shots_at_min_magnitude'],
            'recovery_acceleration': data_fire_mode['recoil_recovery_acceleration'],
            'recovery_delay': data_fire_mode['recoil_recovery_delay_ms']/1000,
            'recovery_rate': data_fire_mode['recoil_recovery_rate']
        },
        'reload': {
            'ammo_fill': data_fire_mode['reload_ammo_fill_ms'] / 1000,
            'chamber': data_fire_mode['reload_chamber_ms'] / 1000,
            'time': data_fire_mode['reload_time_ms'] / 1000
        },
        'cof': {
            'min': data_player_state['cof_min'],
            'max': data_player_state['cof_max'],
            'grow_rate': data_player_state['cof_grow_rate'],
            'recovery_delay': data_player_state['cof_recovery_delay_ms']/1000,
            'recovery_rate': data_player_state['cof_recovery_rate'],
            'recovery_delay_threshold': data_player_state['cof_recovery_delay_threshold'],
            'turn_penalty': data_player_state['cof_turn_penalty'],
            'pellet_spread': data_fire_mode['cof_pellet_spread'],
            'range': data_fire_mode['cof_range'],
            'recoil': data_fire_mode['cof_recoil'],
            'scalar': data_fire_mode['cof_scalar'],
            'scalar_moving': data_fire_mode['cof_scalar_moving']
        },
        'fire': {
            'ammo_per_shot': data_fire_mode["fire_ammo_per_shot"],
            'time_auto_fire': data_fire_mode["fire_auto_fire_ms"] / 1000,
            'burst_count': data_fire_mode["fire_burst_count"],
            'time_charge_up': data_fire_mode["fire_charge_up_ms"] / 1000,
            'time_delay': data_fire_mode["fire_delay_ms"] / 1000,
            'detect_range': data_fire_mode["fire_detect_range"],
            'time_refire': data_fire_mode["fire_refire_ms"] / 1000,
            'pellets_per_shot': data_fire_mode["fire_pellets_per_shot"]
        },
        'attachments': attachments
    }
    '''

    # Extract attachment stats
    # TODO: Add zoom and zoom modifiers
    att_values = {}
    for att_name in attachments:
        # Filter attachments
        att_stats = ps2.utils.filter_list(data['full']['attachments'], name=att_name)
        # Apply effects
        for effect in att_stats[0]['effect']:
            if len(ps2.utils.filter_list(constants.ATT_MODIFIERS.values(), var=effect['StatId'])) > 0:
                if 'PcntAddend' in effect.keys():
                    val = effect['PcntAddend']/100
                else:
                    val = effect['Addend']
                if val != 0:
                    att_values[effect['StatId']] = val

    stats = build_stats(data, att_values)
    stats['attachments'] = attachments

    return stats


def build_stats(data:dict, att_values:dict):
    """
    Creates dictionary of weapon stats based on pre-defined stats mapping

    :param data: Dictionary of segmented weapon data
    :param att_values: Dictionary of attachment parameter names and values
    :return: Dictionary of weapon stats
    """
    stats = {}
    for primary_key, primary_val in constants.WEAPON_MAPPING.items():
        if isinstance(primary_val, list):
            stats[primary_key] = ps2.utils.val_from_dict(data, primary_val)
            continue

        stats[primary_key] = {}
        for secondary_key, stat_path in primary_val.items():
            val = ps2.utils.val_from_dict(data, stat_path)
            cur_path = (primary_key, secondary_key)
            if cur_path in constants.ATT_MODIFIERS.keys():
                func = constants.ATT_MODIFIERS[cur_path]['operation']
                var_name = constants.ATT_MODIFIERS[cur_path]['var']
                if var_name in att_values.keys():
                    val = func((val, att_values[var_name]))
            if stat_path[-1][-3:] == '_ms':
                val /= 1000
            stats[primary_key][secondary_key] = val

    return stats


if __name__ == '__main__':
    #download_weapon(70998)
    extract_stats(70998, attachments=['Soft Point Ammunition', 'High Velocity Ammunition', 'NiCO (1x)', 'Compensator', 'Forward Grip', 'Laser Sight'])
