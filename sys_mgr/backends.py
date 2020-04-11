from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print(username, password)
        try:
            user = User.objects.get(name=username)
            if user.password == password:
                print('auth ok')
                return user
        except User.DoesNotExist:
            return None
        print('auth error')
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
#    def has_perm(self, user_obj, perm, obj=None):
#        return True 

#    def has_module_perms(self, user_obj, app_label):
#        return True
