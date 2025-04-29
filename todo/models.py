from mongoengine import Document, StringField, BooleanField, ReferenceField, DateTimeField, ListField
from django.utils import timezone
from mongoengine import ValidationError

class Task(Document):
    title = StringField(required=True)
    description = StringField()
    status = StringField(default="pending", choices=["pending", "in-progress", "completed"])
    due_date = DateTimeField()
    priority = StringField(choices=["low", "medium", "high"], default="medium")
    linked_task = ReferenceField('self', required=False, null=True)
    created_at = DateTimeField(default=timezone.now)

    def clean(self):

        if self.linked_task and self.status == "completed" and self.linked_task.status != "completed":
            raise ValidationError(f"Cannot complete task '{self.title}' until linked task '{self.linked_task.title}' is completed.")

    def __str__(self):
        return self.title


class Subtask(Document):
    title = StringField(required=True)
    parent_task = ReferenceField(Task, required=True, reverse_delete_rule=2)
    completed = BooleanField(default=False)
    due_date = DateTimeField()
    priority = StringField(choices=["low", "medium", "high"], default="medium")
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} (Subtask of {self.parent_task.title})"


class Comment(Document):
    user_name = StringField(required=True)
    text = StringField(required=True)
    task = ReferenceField(Task, null=True)
    subtask = ReferenceField(Subtask, null=True)
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user_name}"


class ActivityLog(Document):
    action = StringField(required=True)
    task = ReferenceField(Task, null=True)
    subtask = ReferenceField(Subtask, null=True)
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Activity at {self.created_at}"
