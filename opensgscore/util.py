from typing import Any


def dict_find_keys(d: dict, v: Any) -> list:
    """
    Find all keys in a dictionary that have the specified value.
    """
    return [k for k, val in d.items() if val == v]