from rest_framework_mongoengine import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from mongoengine import ValidationError as MEValidationError

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

    def perform_create(self, serializer):
        try:
            serializer.save()
        except MEValidationError as e:
            raise ValidationError({"detail": str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save()
        except MEValidationError as e:
            raise ValidationError({"detail": str(e)})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Task '{title}' has been deleted."},
            status=status.HTTP_200_OK
        )


class SubtaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        task_pk = self.kwargs.get('task_pk')
        if task_pk:
            return Subtask.objects.filter(parent_task=task_pk)
        return Subtask.objects.all()

    def perform_create(self, serializer):
        try:
            task_pk = self.kwargs.get('task_pk')
            if task_pk:
                parent = Task.objects.get(pk=task_pk)
                serializer.save(parent_task=parent)
            else:
                serializer.save()
        except Task.DoesNotExist:
            raise ValidationError({"parent_task": "Specified task does not exist."})
        except MEValidationError as e:
            raise ValidationError({"detail": str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save()
        except MEValidationError as e:
            raise ValidationError({"detail": str(e)})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Subtask '{title}' has been deleted."},
            status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
