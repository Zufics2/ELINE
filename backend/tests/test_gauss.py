import unittest
from fractions import Fraction

from solvers import get_solver
from solvers.base import SolverInputError


def run(matrix, mode="gauss"):
    return get_solver("gauss").solve({"matrix": matrix, "mode": mode})


class GaussTests(unittest.TestCase):
    def test_unique(self):
        out = run([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
        self.assertEqual(out["result"]["type"], "unique")
        self.assertEqual(out["result"]["solution"], {"x_1": "2", "x_2": "3", "x_3": "-1"})
        self.assertEqual(out["result"]["rank"], 3)

    def test_unique_jordan(self):
        out = run([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]], "gauss_jordan")
        self.assertEqual(out["result"]["solution"], {"x_1": "2", "x_2": "3", "x_3": "-1"})

    def test_row_swap(self):
        out = run([[0, 1, 3], [1, 0, 2]])
        self.assertTrue(any("Swap" in s["title"] for s in out["steps"]))
        self.assertEqual(out["result"]["solution"], {"x_1": "2", "x_2": "3"})

    def test_fractions(self):
        out = run([["1/2", 1, 2], [1, "1/3", 1]])
        self.assertEqual(out["result"]["type"], "unique")
        self.assertEqual(Fraction(out["result"]["solution"]["x_1"]), Fraction(2, 5))
        self.assertEqual(Fraction(out["result"]["solution"]["x_2"]), Fraction(9, 5))

    def test_infinite(self):
        out = run([[1, 1, 2], [2, 2, 4]])
        self.assertEqual(out["result"]["type"], "infinite")
        self.assertEqual(out["result"]["free_variables"], ["x_2"])
        self.assertEqual(out["result"]["solution"]["x_1"], "2 - t_1")

    def test_inconsistent(self):
        out = run([[1, 1, 2], [2, 2, 5]])
        self.assertEqual(out["result"]["type"], "none")

    def test_invalid_input(self):
        solver = get_solver("gauss")
        for bad in ({"matrix": []}, {"matrix": [[1, 2], [3]]}, {"matrix": [[1]]}, {"matrix": [["a", 1]]}):
            with self.assertRaises(SolverInputError):
                solver.validate(bad)

    def test_steps_have_contract_fields(self):
        for s in run([[1, 2, 3], [4, 5, 6]])["steps"]:
            self.assertEqual(set(s), {"index", "title", "description", "operation", "matrix", "meta"})
