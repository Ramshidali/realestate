from django import template
from django.db.models import Q, Sum
from django.contrib.auth.models import User, Group

from admin_user.models import AdminUser

register = template.Library()

@register.simple_tag
def get_username(request):
    user = User.objects.get(username=request.user.username)
    if user.is_superuser==True:
        username = request.user.username
        user_image = ""
    else:
        admin_instances = AdminUser.objects.get(user=user)
        username = admin_instances.get_fullname()
        user_image = admin_instances.image
        
    return {
        'username': username,
        'user_image': user_image,
    }