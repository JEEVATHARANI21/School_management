from django.contrib import admin
from .models import Role, Permission, RolePermission

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status')
    search_fields = ('name', 'slug')
    list_filter = ('status',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status')
    search_fields = ('name', 'slug')
    list_filter = ('status',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'status')
    list_filter = ('status', 'role')
    search_fields = ('role__name', 'permission__name')
