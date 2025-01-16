from enum import Enum

from django.contrib.auth.models import AbstractUser
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

class AppUser(AbstractUser):
        email = models.EmailField(unique=True)
        username = models.CharField(max_length=30, unique=True)
        password = models.CharField(max_length=128)
        last_login = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)
        is_superuser = models.BooleanField(default=False)
        first_name = models.CharField(max_length=30, blank=True)
        last_name = models.CharField(max_length=30, blank=True)
        is_staff = models.BooleanField(default=False)
        date_joined = models.DateTimeField(auto_now_add=True)

        class Meta:
            db_table = 'app_user'

def __str__(self):
    return self.username

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    due_date = models.DateTimeField(max_length=50)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
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
    user = models.ManyToManyField(AppUser, related_name='tasks')

    class Meta:
        db_table = 'task'


