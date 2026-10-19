"""Helpers that turn numbers, matrices and row operations into LaTeX."""
from fractions import Fraction


def frac(f: Fraction) -> str:
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f < 0 else ""
    return f"{sign}\\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def matrix(rows, augmented=False) -> str:
    """Matrix as LaTeX; with augmented=True the last column is set off by a bar."""
    ncols = len(rows[0])
    spec = "c" * (ncols - 1) + ("|c" if augmented else "c")
    body = " \\\\ ".join(" & ".join(frac(v) for v in row) for row in rows)
    return f"\\left[\\begin{{array}}{{{spec}}} {body} \\end{{array}}\\right]"


def row_term(coef: Fraction, row: int) -> str:
    """`coef` (> 0) times row R_row, omitting a coefficient of 1."""
    coef = Fraction(coef)
    prefix = "" if coef == 1 else frac(coef)
    return f"{prefix}R_{{{row + 1}}}"
