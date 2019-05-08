from django import template
from collections import OrderedDict
import re
register = template.Library()

@register.inclusion_tag('menu.html')
def menu(request):
    cur_url=request.path_info
    order_dict=OrderedDict()
    menu=request.session.get('menu')
    menu_weight_list=sorted(menu,key=lambda x:menu[x]['weight'])
    for i in menu_weight_list:
        j=order_dict[i]=menu[i]
        j['class'] = 'hide'
        for m in j['children']:
            if m['id'] == request.cur_menu_url:
                j['class'] = ''
                m['class'] = 'active'

    # for j in order_dict.values():
    #     j['class']='hide'
    #     for m in j['children']:
    #         if m['id']==request.cur_menu_url:
    #             j['class'] = ''
    #             m['class'] = 'active'

    return {'menu_list':order_dict.values()}

@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list=request.breadcrumb_list
    return {'breadcrumb_list': breadcrumb_list}

@register.filter
def has_permission(request,name):
    if name in request.session['permission']:
        return True

@register.simple_tag
def gen_role_url(request, rid):
	params = request.GET.copy()
	params['rid'] = rid
	return params.urlencode()
