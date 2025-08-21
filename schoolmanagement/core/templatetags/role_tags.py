from django import template
from ..models import Newregester, Teacher , Student , Class , Event , Role ,Permission, RolePermission


register = template.Library()

@register.filter
def check_role(request, role):
    return request.session.get('role') == role
