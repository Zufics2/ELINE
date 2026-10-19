# Importing a module registers its solver. Add new methods here.
from . import gauss  # noqa: F401
from .registry import UnknownMethod, get_solver, list_solvers  # noqa: F401
