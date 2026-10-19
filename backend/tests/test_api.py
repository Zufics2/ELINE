from unittest import mock

from django.test import TestCase
from rest_framework.test import APIClient


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_methods(self):
        res = self.client.get("/api/methods/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["key"], "gauss")

    def test_solve_and_history(self):
        body = {"method": "gauss", "input": {"matrix": [[1, 1, 3], [1, -1, 1]]}}
        res = self.client.post("/api/solutions/", body, format="json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["result"]["solution"], {"x_1": "2", "x_2": "1"})
        self.assertGreater(len(data["steps"]), 1)
        self.assertEqual(len(self.client.get("/api/solutions/").json()), 1)
        self.assertEqual(self.client.get(f"/api/solutions/{data['id']}/").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/solutions/{data['id']}/").status_code, 204)

    def test_validation_errors(self):
        res = self.client.post("/api/solutions/", {"method": "nope", "input": {}}, format="json")
        self.assertEqual(res.status_code, 400)
        res = self.client.post(
            "/api/solutions/", {"method": "gauss", "input": {"matrix": [["x", 1]]}}, format="json"
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("input", res.json())

    def test_async_returns_202_and_task_is_pollable(self):
        body = {"method": "gauss", "input": {"matrix": [[1, 2], [3, 4]]}, "run_async": True}
        with mock.patch("apps.solutions.services.solve_task.apply_async") as queued:
            res = self.client.post("/api/solutions/", body, format="json")
        self.assertEqual(res.status_code, 202)
        queued.assert_called_once()
        poll = self.client.get(f"/api/tasks/{res.json()['task_id']}/")
        self.assertEqual(poll.json()["status"], "pending")

    def test_task_runs(self):
        from apps.solutions.models import Solution
        from apps.solutions.tasks import solve_task

        sol = Solution.objects.create(method="gauss", input={"matrix": [[1, 1], [0, 1]]}, status="pending")
        solve_task(sol.pk)
        sol.refresh_from_db()
        self.assertEqual(sol.status, "done")
