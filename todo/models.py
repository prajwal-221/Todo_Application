from mongoengine import Document, StringField, BooleanField, ReferenceField, DateTimeField
from django.utils import timezone

class Task(Document):
    title = StringField(required=True)
    description = StringField()
    status = StringField(default="pending", choices=["pending", "in-progress", "completed"])
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Subtask(Document):
    title = StringField(required=True)
    parent_task = ReferenceField(Task, required=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} (Subtask of {self.parent_task.title})"
