from celery import shared_task

from solvers import get_solver


@shared_task(ignore_result=True)
def solve_task(solution_id: int) -> None:
    from .models import Solution
    from .services import apply_result

    solution = Solution.objects.get(pk=solution_id)
    try:
        apply_result(solution, get_solver(solution.method).solve(solution.input))
    except Exception as exc:  # noqa: BLE001 - store any failure for the client
        solution.status = Solution.Status.FAILED
        solution.error = str(exc)
    solution.save()
