from django.urls import path

from mgtapi.views import get_users, create_user, delete_data, put_data, post_data, get_data

urlpatterns = [
    path('task/get', get_data, name='Get tasks'),
    path('task/create', post_data, name='post tasks'),
    path('task/update/<int:id>', put_data, name='update tasks'),
    path('task/delete/<int:pk>', delete_data, name='delete task'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create', create_user, name='create user'),
    path('users/', get_users, name='get users'),
]