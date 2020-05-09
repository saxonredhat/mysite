from django.urls import path
from .views import IndexView, UserListView, RoleListView, PermissionListView, MenuListView, SpaceListView, LoginView

app_name = "sys_mgr"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserListView.as_view(), name='user'),
    path('role', RoleListView.as_view(), name='role'),
    path('permission', PermissionListView.as_view(), name='permission'),
    path('menu', MenuListView.as_view(), name='menu'),
    path('space', SpaceListView.as_view(), name='space'),
    path('ticket/add', IndexView.as_view(), name='ticket'),
    path('ticket/list', IndexView.as_view(), name='ticket'),
    path('ticket/audit/list', IndexView.as_view(), name='ticket'),
    path('ticket/task/list', IndexView.as_view(), name='ticket'),
]