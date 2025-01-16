from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mgtapi.auth import get_username_from_jwt
from mgtapi.models import Task, AppUser
from mgtapi.serializers import TaskSerializer, AppUserSerializer

@api_view(['GET'])
def get_data(request):
    validate_user_permission(request)
    queryset = Task.objects.all().filter(user=request.user.id)
    serializer = TaskSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_data(request):
    app_user= validate_user_permission(request)
    data = request.data
    data['user'] = {app_user['id']}
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Task created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def put_data(request, id):
    validate_user_permission(request)
    try:
        task = Task.objects.get(id=id)
        # if task.status == Status.COMPLETED:
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_data(request, pk):
    validate_user_permission(request)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    validate_user_permission(request)
    queryset = AppUser.objects.all()
    serializer = AppUserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    data = request.data
    request.data['password'] = make_password(request.data['password'])
    serializer = AppUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_filtered_status_priority_due_date(request):
    validate_user_permission(request)
    filter=request.data.get('filter')
    value=request.data.get('value')

    if filter=='status':
        status_filter=Task.objects.filter(status=value)
        serializer=TaskSerializer(status_filter, many=True)
        return Response(serializer.data)
    elif filter=='priority':
        priority_filter=Task.objects.filter(priorityLevel=value)
        serializer=TaskSerializer(priority_filter, many=True)
        return Response(serializer.data)
    elif filter=='due_date':
        due_date_filter=Task.objects.filter(due_date__lte=date.today())
        serializer=TaskSerializer(due_date_filter, many=True)
        return Response(serializer.data)
    elif filter=='sort':
        tasks=Task.objects.all().order_by(value)
        print(tasks.count())
        serializer=TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif filter=='sort#':
        tasks=Task.objects.all().order_by(value).reverse()
        serializer=TaskSerializer(tasks, many=True)
        return Response(serializer.data)

def get_username_from_token_from_request(request):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token= auth_header.split(" ")[1]
        return get_username_from_jwt(token)
    return None

def validate_user_permission(request):
    user_id = get_username_from_token_from_request(request)
    app_user = AppUserSerializer(request.user).data
    if user_id != app_user['id']:
        return Response('You are not authorized to access this resource', status=status.HTTP_200_OK)
    return app_user