_REGISTRY = {}


class UnknownMethod(KeyError):
    pass


def register(cls):
    """Class decorator: instantiate the solver and add it to the registry."""
    _REGISTRY[cls.key] = cls()
    return cls


def get_solver(key):
    try:
        return _REGISTRY[key]
    except KeyError:
        raise UnknownMethod(key) from None


def list_solvers():
    return list(_REGISTRY.values())
