import itertools
from typing import Iterable, Optional, List, Dict, Set


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
    idx = int
    name: Optional[str]

    def __init__(self, idx:int,  name:Optional[str]=None):
        self.idx = idx
        self.name = name


class Graph:
    inputs: Set[Input]
    evaluations: Dict[callable, dict]
    eval_order: List[Operation]
    names: Dict[Operation or Input, str]

    def __init__(self, final_operation:Operation):
        # Initialize set for inputs
        self.inputs = set()
        # Initialize evaluation memory
        self.evaluations = dict()
        # Initialize list for evaluation order
        self.eval_order = []
        # Initialize dictionary of names
        self.names = {}
        # Determine evaluation order
        self._find_order(final_operation)
        # Get names
        self._get_names()

    def _find_order(self, element):
        # Element is Operation -> recurse, add to order
        if isinstance(element, Operation):
            # Recursively check all argument operations
            for arg in element.arguments:
                self._find_order(arg)
            # Add current operation to evaluation eval_order if not added already
            if element not in self.eval_order:
                self.eval_order.append(element)
            # Add element function to evaluation memory
            self.evaluations[element.function] = {}
        # Element is Input -> add to inputs
        elif isinstance(element, Input):
            self.inputs.add(element)
        # Element is other type -> error
        else:
            raise TypeError('Invalid graph element: {}'.format(element.__class__))

    def _get_names(self):
        for inp in self.inputs:
            name = f'in_{inp.idx}' if inp.name is None else inp.name
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
            values = {inp: combi[inp.idx] for inp in self.inputs}
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
