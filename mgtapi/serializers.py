from datetime import datetime

from django.db import models
from rest_framework import serializers

from mgtapi.models import Task, User


# def validate_fields(due_date):
#     try:
#         # due_date = datetime.strptime(due_date, '%d/%m/%Y').date()
#         if due_date <= date.today().strftime('%Y-%m-%d'):
#             raise serializers.ValidationError("The due date must be in the future.")
#         return True
#     except ValueError:
#         print("Invalid due date")
#         return False


def validate_fields(val):
    # Implement your custom validation logic here
    # For example, check if the date is in the future
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
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_val')
        ]
        model = User
        fields = ['id', 'username', 'email', 'password', 'tasks']