from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import User, Menu
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
        #存在则、判断密码是否正确
        if user:
            if password == user.password:
                # 密码正确则，获取用户对应的权限列表
                _perm_url_list = user.get_perm_url_list()
                request.session['perm_list'] = _perm_url_list
                print(_perm_url_list)
                #菜单列表写入到session

                #循环获取子菜单
                _menu_obj_list = []
                for menu in Menu.objects.filter(parent_menu__isnull=False):
                    _sub_menu_list = []
                    for perm_url in _perm_url_list:
                        if re.match("^"+perm_url+"$", menu.url):
                            _menu_obj_list.append(menu.url)
                            # 构建_sub_menu_obj
                            #判断_sub_menu_list是否存在_menu_obj对应的名字
                            #不存在构建_menu_obj对象，创建_sub_menu_list
                            #存在取出对应的_menu_obj的_sub_menu_list append _sub_menu_obj

                            _sub_menu_obj = {}
                print("拥有的菜单url:"+str(_menu_obj_list))
                return render(request, 'main.html')

        return render(request, 'login.html')


class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'index.html')


class RoleView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'role.html')


class UserView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'user.html')


class MenuView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'menu.html')


class PermissionView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'permission.html')


class PermissionGroupView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'main.html')
