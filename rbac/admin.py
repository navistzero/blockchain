from django.contrib import admin
from rbac import models

class PermissionAdmin(admin.ModelAdmin):
    list_display=['id','title','url','parent','url_name']
    list_editable=['title','url','parent','url_name']

class RoleAdmin(admin.ModelAdmin):
    list_display=['id','name']
    list_editable=['name']

# class UserAdmin(admin.ModelAdmin):
#     list_display=['id','name']
#     list_editable=['name']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id','title','icon','weight']
    list_editable = ['title','icon','weight']

admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role,RoleAdmin)
# admin.site.register(models.User,UserAdmin)
admin.site.register(models.Menu,MenuAdmin)