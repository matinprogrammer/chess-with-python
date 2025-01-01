from typing import Iterable


def is_instance_list(iterable: Iterable, element_type=Iterable):
    if not isinstance(iterable, Iterable):
        raise TypeError(f"you must pass a iterable not {type(iterable)}")

    return all(isinstance(item, element_type) for item in iterable)
