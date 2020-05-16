from .models import User


def get_user(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        user = None
    return user