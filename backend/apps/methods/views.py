from rest_framework.response import Response
from rest_framework.views import APIView

from solvers import list_solvers


class MethodListView(APIView):
    def get(self, request):
        return Response([s.describe() for s in list_solvers()])
