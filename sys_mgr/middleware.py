import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from django.conf import settings

class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        #设置白名单
        for white_url in settings.SYSMGR_WHITE_URL:
            if re.search(white_url, current_url):
                return None

        #检验是否登录
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/sys_mgr/login")

        perm_url_list = request.session.get("perm_url_list")
        print('current_url:'+current_url)
        print('perm_url_list:' + str(perm_url_list))
        #校验权限
        for perm_url in perm_url_list:
            if re.match(perm_url, current_url):
                return None
        return HttpResponse("无访问权限！")
