from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Task, Subtask, Comment, ActivityLog


class TaskSerializer(DocumentSerializer):
    linked_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Task
        fields = '__all__'


class SubtaskSerializer(DocumentSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class CommentSerializer(DocumentSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ActivityLogSerializer(DocumentSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'
