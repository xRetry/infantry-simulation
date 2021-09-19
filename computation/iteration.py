from typing import Iterable
import itertools


def iterate(func, args, names_in, names_out, flatten=False):

    summary = {}

    args_wrapped = []
    n_iterations = 0
    for i in range(len(args)):
        arg = args[i]
        if not isinstance(arg, Iterable):
            arg = [arg]
        n_iterations *= len(arg)
        args_wrapped.append(arg)
        summary[names_in[i]] = []

    for name in names_out:
        summary[name] = []

    for inputs in itertools.product(*args_wrapped):
        outputs = func(*inputs)
        if not isinstance(outputs, tuple):
            outputs = [outputs]

        for i in range(len(inputs)):
            if flatten:
                summary[names_in[i]] += [inputs[i] for j in range(len(outputs[0]))]
            else:
                summary[names_in[i]].append(inputs[i])
        for i in range(len(outputs)):
            if flatten:
                summary[names_out[i]] += outputs[i]
            else:
                summary[names_out[i]].append(outputs[i])

    return summary


if __name__ == '__main__':
    pass
