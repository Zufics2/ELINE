"""Gaussian and Gauss-Jordan elimination with exact (rational) arithmetic."""
import math
from fractions import Fraction

import sympy

from . import latex
from .base import BaseSolver, SolverInputError, Step
from .registry import register

MAX_SIZE = 50


def _to_fraction(value) -> Fraction:
    if isinstance(value, bool):
        raise SolverInputError("Matrix entries must be numbers.")
    try:
        if isinstance(value, int):
            return Fraction(value)
        if isinstance(value, float):
            if not math.isfinite(value):
                raise SolverInputError("Matrix entries must be finite.")
            return Fraction(value).limit_denominator(10**9)
        if isinstance(value, str):
            text = value.strip().replace(",", ".")
            if not text or len(text) > 24 or "e" in text.lower():
                raise ValueError
            return Fraction(text)
    except (ValueError, ZeroDivisionError):
        pass
    raise SolverInputError(
        f"Cannot read “{value}” as a number. Use integers, decimals or fractions like 1/3."
    )


def _rat(f: Fraction) -> sympy.Rational:
    return sympy.Rational(f.numerator, f.denominator)


@register
class GaussianEliminationSolver(BaseSolver):
    key = "gauss"
    name = "Gaussian elimination"
    description = "Solve a system of linear equations by row reduction, step by step."
    input_schema = {
        "type": "augmented_matrix",
        "min": 1,
        "max": MAX_SIZE,
        "options": [
            {
                "key": "mode",
                "label": "Variant",
                "default": "gauss",
                "choices": [
                    {"value": "gauss", "label": "Gauss (back substitution)"},
                    {"value": "gauss_jordan", "label": "Gauss–Jordan (reduced form)"},
                ],
            }
        ],
    }

    # ---- validation -------------------------------------------------
    def _parse(self, payload):
        rows = payload.get("matrix") if isinstance(payload, dict) else None
        if not isinstance(rows, list) or not rows or not all(isinstance(r, list) for r in rows):
            raise SolverInputError("Provide “matrix” as a list of rows.")
        width = len(rows[0])
        if any(len(r) != width for r in rows):
            raise SolverInputError("All rows must have the same length.")
        if width < 2:
            raise SolverInputError(
                "The augmented matrix needs at least one variable column and one constants column."
            )
        if len(rows) > MAX_SIZE or width - 1 > MAX_SIZE:
            raise SolverInputError(
                f"The system can have at most {MAX_SIZE} equations and {MAX_SIZE} variables."
            )
        mode = payload.get("mode", "gauss")
        if mode not in ("gauss", "gauss_jordan"):
            raise SolverInputError("Unknown variant. Use “gauss” or “gauss_jordan”.")
        return [[_to_fraction(v) for v in r] for r in rows], mode

    def validate(self, payload):
        self._parse(payload)

    def size_hint(self, payload):
        rows = payload.get("matrix") or []
        if not rows or not isinstance(rows[0], list):
            return 0
        return max(len(rows), len(rows[0]) - 1)

    # ---- solving ----------------------------------------------------
    def solve(self, payload):
        A, mode = self._parse(payload)
        jordan = mode == "gauss_jordan"
        m, n = len(A), len(A[0]) - 1
        steps: list[Step] = []

        def add(title, description, operation="", matrix=True, meta=None):
            steps.append(
                Step(
                    len(steps) + 1,
                    title,
                    description,
                    operation,
                    latex.matrix(A, augmented=True) if matrix else "",
                    meta or {},
                )
            )

        add("Augmented matrix", "Write the system as an augmented matrix; the bar separates the constants.")

        pivots = []  # (row, col)
        r = 0
        for c in range(n):
            if r >= m:
                break
            p = next((i for i in range(r, m) if A[i][c] != 0), None)
            if p is None:
                add(
                    f"Column {c + 1} has no pivot",
                    f"Every entry in column {c + 1} from row {r + 1} down is zero, so x_{c + 1} is a free variable.",
                    meta={"column": c},
                )
                continue
            if p != r:
                A[r], A[p] = A[p], A[r]
                add(
                    f"Swap rows {r + 1} and {p + 1}",
                    f"The entry in row {r + 1}, column {c + 1} is zero, so bring up a row with a non-zero pivot.",
                    f"R_{{{r + 1}}} \\leftrightarrow R_{{{p + 1}}}",
                    meta={"pivot": [r, c]},
                )
            pivots.append((r, c))

            if jordan and A[r][c] != 1:
                factor = 1 / A[r][c]
                A[r] = [v * factor for v in A[r]]
                term = ("-" if factor < 0 else "") + latex.row_term(abs(factor), r)
                add(
                    f"Scale row {r + 1}",
                    f"Divide row {r + 1} by the pivot to make it 1.",
                    f"R_{{{r + 1}}} \\leftarrow {term}",
                    meta={"pivot": [r, c]},
                )

            for i in range(m) if jordan else range(r + 1, m):
                if i == r or A[i][c] == 0:
                    continue
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
                sign, mag = ("-", f) if f > 0 else ("+", -f)
                add(
                    f"Eliminate x_{c + 1} from row {i + 1}",
                    f"Use the pivot in row {r + 1} to zero out column {c + 1} in row {i + 1}.",
                    f"R_{{{i + 1}}} \\leftarrow R_{{{i + 1}}} {sign} {latex.row_term(mag, r)}",
                    meta={"pivot": [r, c], "row": i},
                )
            r += 1

        rank = len(pivots)
        pivot_cols = {c for _, c in pivots}
        free_cols = [c for c in range(n) if c not in pivot_cols]
        bad = next((i for i in range(m) if all(v == 0 for v in A[i][:n]) and A[i][n] != 0), None)

        if bad is not None:
            add(
                "Inconsistent system",
                f"Row {bad + 1} reads 0 = {latex.frac(A[bad][n])}, which is impossible. The system has no solution.",
                f"0 = {latex.frac(A[bad][n])}",
                meta={"row": bad},
            )
            return self._finish(steps, "none", rank, n, {}, [], "\\text{No solution}")

        # Back substitution (also used to read the solution in Gauss-Jordan form)
        t_syms = {c: sympy.Symbol(f"t_{k + 1}") for k, c in enumerate(free_cols)}
        values = dict(t_syms)
        for row, col in reversed(pivots):
            expr = _rat(A[row][n]) - sum(
                (_rat(A[row][j]) * values[j] for j in range(col + 1, n)), sympy.Integer(0)
            )
            values[col] = sympy.expand(expr / _rat(A[row][col]))
            if not jordan:
                add(
                    f"Back substitution: x_{col + 1}",
                    f"Solve row {row + 1} for x_{col + 1} using the variables already found.",
                    f"x_{{{col + 1}}} = {sympy.latex(values[col])}",
                    matrix=False,
                    meta={"pivot": [row, col]},
                )

        solution = {f"x_{c + 1}": str(values[c]) for c in range(n)}
        lines = " \\\\ ".join(
            f"x_{{{c + 1}}} &= {sympy.latex(values[c])}"
            + (f"\\quad (\\text{{free}})" if c in t_syms else "")
            for c in range(n)
        )
        result_latex = f"\\begin{{aligned}} {lines} \\end{{aligned}}"
        if jordan:
            add(
                "Read off the solution",
                "The matrix is in reduced row echelon form, so each pivot row gives its variable directly.",
                result_latex,
            )
        kind = "infinite" if free_cols else "unique"
        return self._finish(
            steps, kind, rank, n, solution, [f"x_{c + 1}" for c in free_cols], result_latex
        )

    @staticmethod
    def _finish(steps, kind, rank, n, solution, free_vars, result_latex):
        return {
            "steps": [s.to_dict() for s in steps],
            "result": {
                "type": kind,  # unique | infinite | none
                "rank": rank,
                "variables": n,
                "free_variables": free_vars,
                "solution": solution,
            },
            "result_latex": result_latex,
        }
