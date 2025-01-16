from datetime import datetime

from django.db import models
from rest_framework import serializers

from mgtapi.models import Task, AppUser


def validate_fields(val):
    if val < datetime.now().strftime('%Y-%m-%d'):
        return False
    return True

class TaskSerializer(serializers.ModelSerializer):
    def validate(self, data):
        due_date = data.get('due_date')
        if due_date:
            formatted_date = due_date.strftime('%Y-%m-%d')
            if not validate_fields(formatted_date):
                raise serializers.ValidationError("Invalid due date: due date must be in the format YYYY-mm-DD and in future")
            data['due_date'] = formatted_date
        else:
            raise serializers.ValidationError("Due date is required.")

        return data

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priorityLevel', 'user']

class AppUserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_val')
        ]
        model = AppUser
        fields = ['id', 'username', 'email', 'password', 'tasks']