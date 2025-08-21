from django import template
from ..models import Newregester, Teacher , Student , Class , Event , Role ,Permission, RolePermission


register = template.Library()

@register.filter
def check_permission(request, permission):
    finduserole = Role.objects.filter(slug=request.session.get('role')).first()
    findpermission = Permission.objects.filter(slug=permission).first()
    checkpermission = RolePermission.objects.filter(role_id=finduserole.id,permission_id=findpermission.id).first()
    return checkpermission.status == 1
