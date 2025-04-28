from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from .models import Task, Subtask, Comment, ActivityLog
from .serializers import (
    TaskSerializer,
    SubtaskSerializer,
    CommentSerializer,
    ActivityLogSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_update(self, serializer):
        old = Task.objects.get(id=serializer.instance.id)
        new_status = serializer.validated_data.get('status', old.status)
        serializer.save()
        # log status change
        if new_status != old.status:
            ActivityLog.objects.create(
                action="status_update",
                task=serializer.instance,
                details=f"Status changed from {old.status} to {new_status}"
            )


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def perform_update(self, serializer):
        old = Subtask.objects.get(id=serializer.instance.id)
        new_completed = serializer.validated_data.get('completed', old.completed)
        serializer.save()
        if new_completed != old.completed:
            ActivityLog.objects.create(
                action="status_update",
                subtask=serializer.instance,
                details=f"Completion changed from {old.completed} to {new_completed}"
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        ActivityLog.objects.create(
            action="comment_added",
            task=comment.task,
            subtask=comment.subtask,
            details=f"Comment added: {comment.content}"
        )


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only listing of all log entries."""
    queryset = ActivityLog.objects.order_by('-timestamp')
    serializer_class = ActivityLogSerializer
