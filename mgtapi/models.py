from enum import Enum

from django.db import models


class Status(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    @classmethod
    def choices(cls):
        return [(status.value, status.name.title()) for status in cls]

class PriorityLevel(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    @classmethod
    def choices(cls):
        return [(status.value, status.name.title()) for status in cls]

class User(models.Model):
        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        password = models.CharField(max_length=255)

        class Meta:
            db_table = 'app_user'

def __str__(self):
    return self.username

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    due_date = models.DateTimeField(max_length=50)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices(),
        default=Status.PENDING.value,
    )
    priorityLevel = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices(),
        default=PriorityLevel.LOW.value
    )
    user = models.ManyToManyField(User, related_name='tasks')
    class Meta:
        db_table = 'task'


