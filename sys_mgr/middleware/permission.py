import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from django.conf import settings

class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        has_perm = False
        permission_urls = []
        for permission_url in permission_urls:
            if re.match(permission_url, current_url):
                has_perm = True

        if not has_perm:
            return HttpResponse("no permission!")
        return None
