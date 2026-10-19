"""Service layer: decides sync vs. Celery, runs solvers, stores history."""
import uuid

from django.conf import settings

from solvers import get_solver

from .models import Solution
from .tasks import solve_task


def apply_result(solution: Solution, output: dict) -> None:
    solution.steps = output["steps"]
    solution.result = output["result"]
    solution.result_latex = output.get("result_latex", "")
    solution.status = Solution.Status.DONE
    solution.error = ""


def create_solution(method: str, input_data: dict, run_async: bool = False):
    """Validate and solve. Returns (solution, queued)."""
    solver = get_solver(method)
    solver.validate(input_data)

    if run_async or solver.size_hint(input_data) > settings.SOLVE_ASYNC_THRESHOLD:
        task_id = str(uuid.uuid4())
        solution = Solution.objects.create(
            method=method, input=input_data, status=Solution.Status.PENDING, task_id=task_id
        )
        solve_task.apply_async(args=[solution.pk], task_id=task_id)
        solution.refresh_from_db()  # eager mode finishes inside apply_async
        return solution, solution.status == Solution.Status.PENDING

    solution = Solution(method=method, input=input_data)
    apply_result(solution, solver.solve(input_data))
    solution.save()
    return solution, False
