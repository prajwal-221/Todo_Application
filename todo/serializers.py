from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from .models import Task, Subtask, Comment, ActivityLog


class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        if instance.linked_task:
            rep['linked_task'] = str(instance.linked_task.id)
        return rep


class SubtaskSerializer(DocumentSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
    )

    class Meta:
        model = Subtask
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        if instance.parent_task:
            rep['parent_task'] = str(instance.parent_task.id)
        return rep


class CommentSerializer(DocumentSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        if instance.task:
            rep['task'] = str(instance.task.id)
        return rep


class ActivityLogSerializer(DocumentSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = str(instance.id)
        if instance.task:
            rep['task'] = str(instance.task.id)
        return rep
