from rbac.models import Permission,Role,User

class InitPermission():

    def __init__(self,user_obj,request):
        self.user_obj=user_obj
        self.request=request

    def per_init(self):
        permission=self.user_obj.roles.filter(permission__url__isnull=False).values(
                        'permission__url',
                        'permission__title',
                        'permission__is_menu_id',
                        'permission__is_menu__title',
                        'permission__is_menu__icon',
                        'permission__is_menu__weight',
                        'permission__id',
                        'permission__parent_id',
                        'permission__url_name',
                        'permission__parent__url_name',
                    ).distinct()
        permission_dict={}
        menu_dict={}
        for i in permission:
            permission_dict[i['permission__url_name']]={'permission_url': i['permission__url'],
                                    'permission_id':i['permission__id'],
                                    'permission_title':i['permission__title'],
                                    'permission_parent_id':i['permission__parent_id'],
                                    'permission_parent_name':i['permission__parent__url_name'],}
            a = {}
            if i['permission__is_menu_id']:
                a = {'title': i['permission__is_menu__title'],
                     'icon': i['permission__is_menu__icon'],
                     'weight': i['permission__is_menu__weight'],
                     'children': []}
                menu_dict.setdefault(i['permission__is_menu_id'], a)
                menu_dict[i['permission__is_menu_id']]['children'].append(
                    {'title': i['permission__title'],
                     'url': i['permission__url'],
                     'id':i['permission__id']}
                )
        self.request.session['menu']=menu_dict
        self.request.session['permission']=permission_dict
        self.request.session['flag']=1
        self.request.session['cur_user']=self.user_obj.name