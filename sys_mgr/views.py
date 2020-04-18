from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views import View
from .models import *
import re

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        #判断数据库中是否存在
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user:
            if password == user.password:
                request.session['user_id'] = user.id
                _perm_url_list = user.get_perm_url_list()
                request.session['perm_url_list'] = _perm_url_list
                submenu_obj_list = []
                for menu in Menu.objects.filter(parent_menu__isnull=False):
                    for perm_url in _perm_url_list:
                        if re.match("^"+perm_url+"$", menu.url):
                            submenu_obj_list.append(menu)
                menu_list = {}
                for submenu in submenu_obj_list:
                    if submenu.parent_menu.name in menu_list.keys():
                        exist_submenu_list = menu_list[submenu.parent_menu.name]
                        exist_submenu_list.append({"name": submenu.name, "url": submenu.url})
                    else:
                        menu_list[submenu.parent_menu.name] = [{"name": submenu.name, "url": submenu.url}]
                request.session['menu_list'] = menu_list
                print("menu_list" + str(menu_list))
                return render(request, 'index2.html')
        return render(request, 'login.html', {'message': "账号不存在或密码错误!!!"})


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = "user.html"

    def get_context_data(self, **kargs):
        self.request.session['abc'] = 'test'
        return super().get_context_data(**kargs)


class RoleListView(ListView):
    model = Role
    context_object_name = 'roles'
    template_name = "role.html"


class PermissionListView(ListView):
    model = Permission
    context_object_name = 'permissions'
    template_name = "permission.html"


class MenuListView(ListView):
    model = Menu
    context_object_name = 'menus'
    template_name = "menu.html"


class SpaceListView(ListView):
    model = Space
    context_object_name = 'spaces'
    template_name = "space.html"



