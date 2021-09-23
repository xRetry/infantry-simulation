from typing import Iterable, Optional
import itertools


def iterate(func, args:dict, names_out, names_in:Optional[dict]=None, flatten=False):

    summary = {}
    keys = []
    n_iterations = 0
    for k, v in args.items():
        if not isinstance(v, Iterable):
            v = [v]
        n_iterations *= len(v)
        var_name = k
        if names_in is not None:
            name_in = names_in.get(k)
            if name_in is not None:
                var_name = name_in
        args[k] = v
        keys.append(var_name)
        summary[var_name] = []

    for name in names_out:
        summary[name] = []

    for inputs in itertools.product(*args.values()):
        outputs = func(*inputs)
        if not isinstance(outputs, tuple):
            outputs = [outputs]

        for i in range(len(inputs)):
            if flatten:
                summary[keys[i]] += [inputs[i] for j in range(len(outputs[0]))]
            else:
                summary[keys[i]].append(inputs[i])
        for i in range(len(outputs)):
            if flatten:
                summary[names_out[i]] += outputs[i]
            else:
                summary[names_out[i]].append(outputs[i])

    return summary


if __name__ == '__main__':
    pass
