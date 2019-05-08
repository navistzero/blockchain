from django.conf.urls import url
from rbac.views import role,menu


urlpatterns = [
    
    url(r'^role/list/$', role.role_list, name='show_role'),
    url(r'^role/add/$', role.role_add, name='add_role'),
    url(r'^role/edit/(\d+)$', role.role_edit,name='edit_role'),
    url(r'^role/del/(\d+)$', role.role_del,name='del_role'),

    url(r'^power/list/$', menu.power_list,name='show_power'),
    url(r'^menu/add/$', menu.menu_change,name='add_menu'),
    url(r'^menu/edit/(\d+)$', menu.menu_change,name='edit_menu'),
    url(r'^menu/del/(\d+)$', menu.menu_del,name='del_menu'),
    url(r'^power/add/$',menu.power_change,name='add_power'),
    url(r'^power/edit/(\d+)$',menu.power_change,name='edit_power'),
    url(r'^power/del/(\d+)$', menu.power_del, name='del_power'),

    url(r'^multi/power/$', menu.multi_power, name='multi_power'),
    url(r'^distribute/power/$', menu.distribute_power, name='distribute_power'),
]