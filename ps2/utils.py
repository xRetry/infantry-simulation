import json
import requests
import constants


def query_from_api(query:str) -> dict:
    """
    Request provided query from Planetside 2 census API and return response.

    :param query: Full query
    :return: Response as dictionary
    """
    response = requests.get(query)
    data = response.json()
    return data


def params_to_query(table:str, c_limit:int=1000, c_lang:str='en', **args) -> str:
    """
    Compiles a set of parameters to a full Planetside 2 census query.

    :param table:  Table (collection) that should be accessed
    :param c_limit: Number of elements in response
    :param c_lang: Language filter for names and descriptions
    :param args: Additional arguments for filtering
    :return: Full query as string
    """
    query_params = ''
    for k, v in args.items():
        query_params += k + '=' + str(v) + '&'
    return f'http://census.daybreakgames.com/get/ps2/{table}?{query_params}&c:lang={c_lang}&c:limit={c_limit}'


def dict_to_json(data_dict, name, path=None):
    """
    Saves provided dictionary to .json file.

    :param data_dict: Dictionary to be saved
    :param name: File name (without file format)
    :param path: Relative folder path from working directory
    :return: None
    """
    if path is None:
        path = constants.DIR + 'resources\\'
    with open(f'{path}{name}.json','w') as file:
        json.dump(data_dict, file, indent=4)


def json_to_dict(name, path=None):
    """
    Loads .json file as dictionary.

    :param name: File name (without file type)
    :param path: Relative folder path from working directory
    :return: Dictionary of file contents
    """
    if path is None:
        path = constants.DIR + 'resources\\'
    with open(f'{path}{name}.json') as file:
        data = json.load(file)
    return data


def filter_list(data_list:list, **cond) -> list:
    """
    Filters list of dictionary by provided condition.

    :param data_list: List of dictionaries
    :param cond: Filter condition in form of key=value
    :return: List of dictionaries fulfilling the condition
    """
    filtered_list = []
    for key, val in cond.items():
        for entry in data_list:
            entry_val = entry.get(key)
            if entry_val is not None and entry_val == val:
                filtered_list.append(entry)
    return filtered_list


def val_from_dict(data:dict, keys:list):
    """
    Returns value of nested dictionary

    :param data: Nested dictionary
    :param keys: List of keys in correct access order
    :return: Value at bottom of nested dictionary
    """
    val = data
    for key in keys:
        val = val[key]
    return val


def load_table(table_name):
    """
    Requests and saves full table from Planetside 2 census API.

    :param table_name: Name of table (collection) in API
    :return: None
    """
    query = params_to_query(table_name)
    categories = query_from_api(query)
    dict_to_json(categories, table_name)


def unpack_dict(d):
    new = {}
    # Iterate through all items in dictionary
    for key, val in d.items():
        # If dictionary: further unpack
        if isinstance(val, dict):
            val = unpack_dict(val)
        # If list: iterate and unpack
        elif isinstance(val, list):
            for i in range(len(val)):
                val[i] = unpack_dict(val[i])
        # If value: try to convert to float
        else:
            try:
                val = float(val)
            except ValueError:
                pass
        # If name/description: return english entry
        if key == 'en':
            return val

        '''
        Possibly leads to loss of information.
        Same param might always map to same value.
        
        if 'param' in key:
            for k, v in d.items():
                if isinstance(v, dict):
                    val_name = v.get(key)
                    if val_name is not None:
                        key = val_name
                        break
        '''

        # If joined entry: add to corresponding (joined-on) key
        if '_join_' in key:
            key, key2 = key.split('_join_')
            val = {key2: val}
        # Check if key already exists
        old_val = new.get(key)
        if old_val is None or not (isinstance(old_val, list) or isinstance(old_val, dict)):
            # Override if simple value, add if not existing
            new[key] = val
    return new


if __name__ == '__main__':
    # d = {
    #     'key_1': 'val_1',
    #     'key_2': '3',
    #     'key_3': {
    #         'key_4': '9'
    #     },
    #     'key_2_join_key_5': [
    #         {
    #             'key_5': '3',
    #             'key_6': '10'
    #         }
    #     ]
    # }
    d = query_from_api('https://census.daybreakgames.com/get/ps2:v2/item?name.en=*Nanoweave&c:limit=50&c:lang=en&c:join=ability^list:1^on:activatable_ability_id^to:ability_id(ability_type^inject_at:ability_type_id,resource_type^inject_at:resource_type_id,effect^on:ability_id^to:ability_id^list:1(effect_type^inject_at:effect_type_id)),ability^list:1^on:passive_ability_id^to:ability_id(ability_type^inject_at:ability_type_id,resource_type^inject_at:resource_type_id,effect^on:ability_id^to:ability_id^list:1(effect_type^inject_at:effect_type_id))')
    result = unpack_dict(d)
    pass
