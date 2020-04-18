from django.template import Library
import re
register =Library()   # 必须命名为 register


# 该自定义过滤器标签不仅给menu.html中传值permission_menu_list，
# 而且还根据列表中的url是否为当前路径，给其添加键值对class=acitve，给菜单列表添加样式

@register.inclusion_tag("sidebar_menu.html")
def get_menu_styles(request):
    menu_list = request.session.get("menu_list")
    return {"menu_list": menu_list}  # 会传值给上面的 rbac/menu.html中，此处类似于render的传值