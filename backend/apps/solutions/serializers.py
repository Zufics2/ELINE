from rest_framework import serializers

from .models import Solution


class SolveRequestSerializer(serializers.Serializer):
    method = serializers.CharField(max_length=64)
    input = serializers.DictField()
    run_async = serializers.BooleanField(required=False, default=False)


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            "id", "method", "input", "steps", "result", "result_latex",
            "status", "error", "task_id", "created_at",
        ]


class SolutionListSerializer(serializers.ModelSerializer):
    result_type = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ["id", "method", "input", "status", "result_type", "created_at"]

    def get_result_type(self, obj):
        return (obj.result or {}).get("type")
