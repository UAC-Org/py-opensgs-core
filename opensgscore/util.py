from typing import Any, Callable


def dict_find_keys(d: dict, v: Any) -> list:
    """
    Find all keys in a dictionary that have the specified value.
    """
    return [k for k, val in d.items() if val == v]


def plant_trigger(*trigger_name: str) -> Callable[[type], type]:
    """
    Decorator to plant triggers.
    """
    def decorator(cls: type) -> type:
        def bind_trigger(self: Any, name: str) -> \
                Callable[[Callable[[Any], None]], None]:
            def trigger(func: Callable[[Any], None]) -> None:
                setattr(self, name, func)
            return trigger
        for trigger in trigger_name:
            setattr(cls, trigger, lambda self: None)
        setattr(cls, "bind_trigger", bind_trigger)
        return cls
    return decorator