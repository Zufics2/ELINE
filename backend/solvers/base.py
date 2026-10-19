"""Contract shared by every solving method.

A solver is plain Python (no Django). It returns a step-by-step solution in a
fixed JSON-friendly format that the frontend renders generically.
"""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field


class SolverInputError(ValueError):
    """Raised when the payload sent to a solver is invalid."""


@dataclass
class Step:
    index: int
    title: str  # "Eliminate column 1"
    description: str  # human-readable explanation
    operation: str = ""  # LaTeX, e.g. "R_2 \\leftarrow R_2 - 2R_1"
    matrix: str = ""  # LaTeX of the matrix after this step ("" = none)
    meta: dict = field(default_factory=dict)  # pivot position, etc.

    def to_dict(self):
        return asdict(self)


class BaseSolver(ABC):
    key: str  # "gauss"
    name: str  # "Gaussian elimination"
    description: str
    # Drives the frontend form. `type` selects the input component,
    # `options` renders extra controls (see frontend/src/methods).
    input_schema: dict

    @abstractmethod
    def validate(self, payload: dict) -> None:
        """Raise SolverInputError if the payload is invalid."""

    @abstractmethod
    def solve(self, payload: dict) -> dict:
        """Return {"steps": [Step.to_dict()...], "result": {...}, "result_latex": "..."}."""

    def size_hint(self, payload: dict) -> int:
        """Rough problem size, used to decide between sync and Celery execution."""
        return 0

    def describe(self) -> dict:
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }
