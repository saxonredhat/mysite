from django.urls import path
from .views import IndexView, RoleView, UserView, LoginView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('role', RoleView.as_view(), name='role'),
    path('user', UserView.as_view(), name='user'),
]