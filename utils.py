import itertools


"""
Collection of useful functions.
"""


def iterate_class(cl:object, name:str) -> zip:
    """
    Recursively converts fields of class into iterator of nested tuples. Returns cartesian product of all list values.

    :param cl: Class object
    :param name: Class name for tuple
    :return: Iterator for nested tuples in form of (field name, field value)
    """
    entries = []
    # Iterate through class fields
    for field_name, field_val in vars(cl).items():
        # Field not nested -> collect
        if isinstance(field_val, (list, tuple)):
            field_name = [field_name for i in range(len(field_val))]
            entries.append(zip(field_name, field_val))
        # Field is the name -> skip
        elif field_name == 'name':
            continue
        # Field is nested -> recurse
        else:
            entries.append(iterate_class(field_val, field_name))
    # Add name to every tuple
    return zip(itertools.cycle([name]), itertools.product(*entries))


def tuple_to_dict(nested:tuple) -> dict:
    """
    Converts nested tuple to dictionary. Used for iterator outputs.

    :param nested: Nested tuple in form of (name, (name, tuple))
    :return: Nested dictionary
    """
    # Check if current value is not a tuple -> return value
    if isinstance(nested[1], tuple):
        return nested[1]
    # Value is tuple -> create dictionary and recurse
    else:
        dct = {}
        for entry in nested[1]:
            dct[entry[0]] = tuple_to_dict(entry)
    return dct


def trace_wrapper(dct:dict, key:str,  value):
    """
    Adds provided key/value entry to 'solution' section in provided dictionary. Creates 'solution' entry if not existent.

    :param dct: Dictionary to be added to (gets mutated)
    :param key: Key under which the value should be added
    :param value: Value to added
    :return: None
    """
    sols = dct.get('solution')
    if sols is None:
        dct['solution'] = dict()
    dct['solution'][key] = value


def aggregate_dict(aggregation_dct:dict, dct:dict):
    """
    Adds all values from dictionary to aggregation dictionary. Appends them to lists in aggregation dict.

    :param aggregation_dct: Dictionary to be aggregated to (gets mutated). Values needs to be lists.
    :param dct: Dictionary from which values are extracted. Structurally identical to aggregation dict.
    :return: None
    """
    # Iterate through all element of dictionary
    for key, val in dct.items():
        # Check if dictionary is nested -> recurse
        if isinstance(val, dict):
            dict_old = aggregation_dct.get(key)
            if dict_old is None:
                dict_old = dict()
            aggregation_dct[key] = aggregate_dict(dict_old, val)
        # Value is not dictionary -> add to aggregation dict
        else:
            val_old = aggregation_dct.get(key)
            if val_old is None:
                aggregation_dct[key] = []
            aggregation_dct[key].append(val)
    return aggregation_dct


if __name__ == '__main__':
    pass
