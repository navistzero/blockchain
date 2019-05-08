from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,reverse,HttpResponse
from django.conf import settings
import re

class RbacMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        cur_url=request.path_info
        request.cur_menu_url=None
        request.breadcrumb_list=[{'title':'首页','url':'/crm/index/'}]

        for i in settings.WHITE_LIST:
            if re.match(i,cur_url):
                return
        
        flag=request.session.get('flag')
        if flag==1:
            for i in settings.NO_PERMISSION_LIST:
                if re.match(i,cur_url):
                    return
            permission=request.session.get('permission')
            # print(cur_url,permission.values())
            for i in permission.values():
                if re.match(r'^{}$'.format(i.get('permission_url')),cur_url):
                    # print(111111)
                    menu_id=i.get('permission_id')
                    menu_parent_id=i.get('permission_parent_id')
                    menu_parent_name=i.get('permission_parent_name')
                    if menu_parent_id:
                        request.cur_menu_url=menu_parent_id
                        request.breadcrumb_list.append({'title':permission[menu_parent_name]['permission_title'],
                                                        'url':permission[menu_parent_name]['permission_url']})
                    else:
                        request.cur_menu_url=menu_id
                    request.breadcrumb_list.append({'title':i['permission_title'],'url':i['permission_url']})
                    return

            return HttpResponse('你无权访问')

        return redirect(reverse('login'))

