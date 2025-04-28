from mongoengine import (
    Document,
    StringField,
    BooleanField,
    ReferenceField,
    DateTimeField,
    ValidationError,
    CASCADE,
)
from django.utils import timezone


class Task(Document):
    title = StringField(required=True)
    description = StringField()
    status = StringField(
        default="pending",
        choices=["pending", "in-progress", "completed"]
    )
    priority = StringField(
        default="medium",
        choices=["low", "medium", "high"]
    )
    due_date = DateTimeField()
    linked_task = ReferenceField(
        'self',
        reverse_delete_rule=CASCADE,
        required=False,    # client may omit
        null=True,         # DB may store None
        default=None       # defaults to None if not provided
    )
    created_at = DateTimeField(default=timezone.now)

    def clean(self):
        # only enforce dependency when linked_task is set
        if (
            self.status == "completed"
            and self.linked_task
            and self.linked_task.status != "completed"
        ):
            raise ValidationError(
                "Cannot complete this task until the linked task is completed."
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subtask(Document):
    title = StringField(required=True)
    parent_task = ReferenceField(Task, reverse_delete_rule=CASCADE, required=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} (Subtask of {self.parent_task.title})"


class Comment(Document):
    content = StringField(required=True)
    created_at = DateTimeField(default=timezone.now)
    task = ReferenceField(Task, reverse_delete_rule=CASCADE, required=False)
    subtask = ReferenceField(Subtask, reverse_delete_rule=CASCADE, required=False)

    def clean(self):
        if not (self.task or self.subtask):
            raise ValidationError("Comment must be linked to a task or a subtask.")
        if self.task and self.subtask:
            raise ValidationError("Comment cannot be linked to both task and subtask.")

    def __str__(self):
        target = self.task.title if self.task else self.subtask.title
        return f"Comment on {target}: {self.content[:20]}"


class ActivityLog(Document):
    ACTION_CHOICES = ["status_update", "comment_added", "other"]
    action = StringField(choices=ACTION_CHOICES, required=True)
    timestamp = DateTimeField(default=timezone.now)
    details = StringField()
    task = ReferenceField(Task, reverse_delete_rule=CASCADE, required=False)
    subtask = ReferenceField(Subtask, reverse_delete_rule=CASCADE, required=False)

    def clean(self):
        if not (self.task or self.subtask):
            raise ValidationError("Log entry must reference a task or a subtask.")
        if self.task and self.subtask:
            raise ValidationError("Log entry cannot reference both task and subtask.")

    def __str__(self):
        target = self.task.title if self.task else self.subtask.title
        return f"{self.timestamp}: {self.action} on {target}"
