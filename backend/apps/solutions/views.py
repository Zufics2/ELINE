from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from solvers import UnknownMethod
from solvers.base import SolverInputError

from .models import Solution
from .serializers import (
    SolutionListSerializer,
    SolutionSerializer,
    SolveRequestSerializer,
)
from .services import create_solution

HISTORY_LIMIT = 50


class SolutionListCreateView(APIView):
    def get(self, request):
        qs = Solution.objects.all()[:HISTORY_LIMIT]
        return Response(SolutionListSerializer(qs, many=True).data)

    def post(self, request):
        req = SolveRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data
        try:
            solution, queued = create_solution(data["method"], data["input"], data["run_async"])
        except UnknownMethod:
            raise ValidationError({"method": f"Unknown method “{data['method']}”."}) from None
        except SolverInputError as exc:
            raise ValidationError({"input": str(exc)}) from None
        code = status.HTTP_202_ACCEPTED if queued else status.HTTP_200_OK
        return Response(SolutionSerializer(solution).data, status=code)


class SolutionDetailView(APIView):
    def get_object(self, pk):
        try:
            return Solution.objects.get(pk=pk)
        except Solution.DoesNotExist:
            raise NotFound("Solution not found.") from None

    def get(self, request, pk):
        return Response(SolutionSerializer(self.get_object(pk)).data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatusView(APIView):
    """Poll a queued solve. Status lives in the DB, so no Celery result backend is needed."""

    def get(self, request, task_id):
        try:
            solution = Solution.objects.only("id", "status", "error").get(task_id=task_id)
        except Solution.DoesNotExist:
            raise NotFound("Task not found.") from None
        return Response(
            {"task_id": task_id, "status": solution.status, "solution_id": solution.id, "error": solution.error}
        )
