from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Task, Subtask

class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubtaskSerializer(DocumentSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'
