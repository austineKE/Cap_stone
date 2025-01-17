from django.urls import path

from mgtapi.auth import CustomTokenObtainPairView
from mgtapi.views import get_users, create_user, delete_data, put_data, post_data, get_data, \
    get_filtered_status_priority_due_date, share_tasks, delete_user

urlpatterns = [
    path('task/get', get_data, name='Get tasks'),
    path('task/create', post_data, name='post tasks'),
    path('task/update/<int:id>', put_data, name='update tasks'),
    path('task/delete/<int:pk>', delete_data, name='delete task'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('user/create', create_user, name='create user'),
    path('users/', get_users, name='get users'),
    path('task/filter', get_filtered_status_priority_due_date, name='get filter'),
    path('task/share', share_tasks, name='share task'),
    path('user/delete/<int:pk>', delete_user, name='delete task'),
]