import itertools
from typing import Iterable, Optional, List, Dict


class Operation:
    name: Optional[str]
    function: callable
    arguments: tuple

    def __init__(self, function:callable, args:tuple, name:Optional[str]=None):
        self.name = name
        self.function = function
        self.arguments = args

    def __call__(self, *args, **kwargs):
        return self.function(*args)


class Input:
    name: Optional[str]

    def __init__(self, name:Optional[str]=None):
        self.name = name


class Graph:
    inputs: Dict[Input, int]
    eval_order: List[Operation]
    names: Dict[Operation or Input, str]

    def __init__(self, inputs:List[Input], final_operation:Operation):
        # Convert list of Inputs to dict of Input->idx
        self.inputs = {inputs[i]:i for i in range(len(inputs))}
        # Initialize list for evaluation order
        self.eval_order = []
        # Initialize dictionary of names
        self.names = {}
        # Determine evaluation order
        self._find_order(final_operation)
        # Get names
        self._get_names()

    def _find_order(self, element):
        # Only continue is current element is Operation
        if isinstance(element, Operation):
            # Recursively check all argument operations
            for arg in element.arguments:
                self._find_order(arg)
            # Add current operation to evaluation eval_order if not added already
            if element not in self.eval_order:
                self.eval_order.append(element)

    def _get_names(self):
        for inp, i in self.inputs.items():
            name = f'in_{i}' if inp.name is None else inp.name
            self.names[inp] = name
        for i, op in enumerate(self.eval_order):
            name = f'op_{i}' if op.name is None else op.name
            self.names[self.eval_order[i]] = name

    def __call__(self, *args, **kwargs):
        # Wrap inputs in list if not already
        args = [a if isinstance(a, Iterable) else [a] for a in args]
        # Initialize list to collect storage dicts
        values_list = []
        # Iterate through all input combinations
        for combi in itertools.product(*args):
            # Create value storage dict with current combination added
            values = {k: combi[v] for k, v in self.inputs.items()}
            # Iterate through ordered evaluation operations
            for operation in self.eval_order:
                # Add evaluation result to storage dict
                values[operation] = operation(*[values[a] for a in operation.arguments])
            # Add complete storage dict to list
            values_list.append(values)
        # Merge storage dicts in list into a singe one
        result = self._merge(values_list)
        # Change keys of dictionary to names
        return self._rename(result)

    def _rename(self, result:Dict[Operation or Input, list]):
        # Initialize output dict
        renamed = {}
        # Iterate through dict entries
        for k, v in result.items():
            # Add current value under name to output dict
            renamed[self.names[k]] = v
        return renamed

    @staticmethod
    def _merge(value_list: List[dict]):
        # Initialize output dict
        merged = {}
        # Iterate through all list entries
        for entry in value_list:
            # Iterate through all dict entries
            for k, v in entry.items():
                # Check if already in dict
                old_entry = merged.get(k)
                # Create new entry if not
                if old_entry is None:
                    merged[k] = [v]
                # Append to value list if yes
                else:
                    merged[k].append(v)
        return merged


if __name__ == '__main__':
    pass
