from django.db import models


class Solution(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        DONE = "done"
        FAILED = "failed"

    method = models.CharField(max_length=64, db_index=True)
    input = models.JSONField()
    steps = models.JSONField(default=list, blank=True)
    result = models.JSONField(null=True, blank=True)
    result_latex = models.TextField(blank=True, default="")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DONE)
    error = models.TextField(blank=True, default="")
    task_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.method} #{self.pk} ({self.status})"
