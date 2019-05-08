from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from crm.models import UserProfile
from rbac.form import MenuForm,PowerForm,MultiPermissionForm
from django.db.models import Q
from django.forms import modelformset_factory,formset_factory

def power_list(request):
    menu_list = models.Menu.objects.all()
    mid=request.GET.get('mid',0)
    if mid:
        power_list = models.Permission.objects.filter(Q(is_menu_id=mid)|Q(parent__is_menu_id=mid)).values('id', 'url',
            'title',
            'url_name',
            'is_menu_id',
            'parent_id',
            'is_menu__title')
    else:
        power_list = models.Permission.objects.all().values('id', 'url',
            'title',
            'url_name',
            'is_menu_id',
            'parent_id',
            'is_menu__title')
    power_dict={}
    for i in power_list:
        if i['is_menu_id']:
            i['children']=[]
            power_dict[i['id']]=i
    for j in power_list:
        if j['parent_id']:
            power_dict[j['parent_id']]['children'].append(j)
    return render(request, 'power_list.html', {'mid':mid,'menu_list': menu_list,'power_list':power_dict.values()})

# def menu_add(request):
#     """
#     新增
#     :return:
#     """
#     if request.method == 'GET':
#         form = MenuForm()
#         return render(request, 'add_role.html', {'form': form})
#     form = MenuForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('rbac:show_power')
#     return render(request, 'add_role.html', {'form': form})
#
# def menu_edit(request, mid):
#     """
#     编辑
#     :return:
#     """
#     obj = models.Menu.objects.get(id=mid)
#     if request.method == 'GET':
#         form = MenuForm(instance=obj)
#         return render(request, 'add_role.html', {'form': form})
#     form = MenuForm(data=request.POST, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect('rbac:show_power')
#     return render(request, 'add_role.html', {'form': form})

def menu_change(request,mid=None):
    obj = models.Menu.objects.filter(id=mid).first()
    if request.method == 'GET':
        form = MenuForm(instance=obj)
        return render(request, 'add_role.html', {'form': form})
    form = MenuForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('rbac:show_power')
    return render(request, 'add_role.html', {'form': form})

def menu_del(request, mid):
    """
    删除角色
    :param request:
    :param cid:
    :return:
    """
    models.Menu.objects.filter(id=mid).delete()
    return redirect('rbac:show_power')

def power_del(request, pid):
    models.Permission.objects.filter(id=pid).delete()
    return redirect('rbac:show_power')


def power_change(request,pid=None):
    obj = models.Permission.objects.filter(pk=pid).first()
    if request.method == 'GET':
        form = PowerForm(instance=obj)
        return render(request, 'add_role.html', {'form': form})
    form = PowerForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('rbac:show_power')
    return render(request, 'add_role.html', {'form': form})

from rbac.server.routes import get_all_url_dict
def multi_power(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    # 删除和编辑使用modelformset
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 添加使用的formset
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    # 获取数据中所有的权限
    permissions = models.Permission.objects.all()
    # 获取到路由系统所有的url（权限）
    router_dict = get_all_url_dict(ignore_namespace_list=['admin'])
    # 数据库中权限别名的集合
    permissions_name_set = set([i.url_name for i in permissions])
    # 路由系统中权限别名的集合
    router_name_set = set(router_dict.keys())
    # 新增权限的别名的集合
    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])
    # print(router_dict)
    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            print('pass')
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            query_list = models.Permission.objects.bulk_create(permission_obj_list)
            add_formset = AddFormSet()
            for i in query_list:
                permissions_name_set.add(i.url_name)
        print('no pass')
    # 删除权限的别名的集合
    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))

    # 更新权限的别名的集合
    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    return render(
        request,
        'multi_powers.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )



def distribute_power(request):
    uid = request.GET.get('uid')  # 用户的id
    rid = request.GET.get('rid')  # 角色的id

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = UserProfile.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permission.set(request.POST.getlist('permissions'))

    # 所有用户
    user_list = UserProfile.objects.all()
    # 用户的角色的id
    user_has_roles = UserProfile.objects.filter(id=uid).values('id', 'roles')
    # 用户所拥有角色id的字典
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    # 所有的角色
    role_list = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid, permission__id__isnull=False).values('id',
                                                                                                        'permission')
    elif uid and not rid:
        user = UserProfile.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.filter(permission__id__isnull=False).values('id', 'permission')
    else:
        role_has_permissions = []
    # 某一个角色所拥有的权限   某一个用户所拥有的所有的权限
    role_has_permissions_dict = {item['permission']: None for item in role_has_permissions}
    # 所有菜单
    all_menu_list = []
    """
     all_menu_list =  [ 
         { id  title  children :[
                 { 'id', 'title', 'menu_id'  'children' : [
                     {'id', 'title', 'parent_id'}
                 ]   } 
         ] }
         {'id': None, 'title': '其他', 'children': [
             {'id', 'title', 'parent_id'}
         ]}
     ]

    """
    queryset = models.Menu.objects.values('id', 'title')  # 一级菜单的id 和 标题  [ { id  title } ]
    # 菜单的字典
    menu_dict = {}
    """
    menu_dict = {
        一级菜单的id： { id  title  children :[
            { 'id', 'title', 'menu_id'  'children' : [
                    {'id', 'title', 'parent_id'}
                ]   } 
        ] },
        None: {'id': None, 'title': '其他', 'children': [
            {'id', 'title', 'parent_id'}
        ]}
    }
    """

    for item in queryset:  # { id  title }
        item['children'] = []  # { id  title  children :[]  }
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other
    # 二级菜单  父权限
    root_permission = models.Permission.objects.filter(is_menu__isnull=False).values('id', 'title', 'is_menu_id')

    root_permission_dict = {}
    """
    root_permission_dict = {
            父权限的id： { 'id', 'title', 'menu_id'  'children' : [
                {'id', 'title', 'parent_id'}
            ]   } 
    }
    """

    for per in root_permission:  # { 'id', 'title', 'menu_id' }
        per['children'] = []  # { 'id', 'title', 'menu_id'  'children' : []   }
        nid = per['id']
        menu_id = per['is_menu_id']
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(is_menu__isnull=True).values('id', 'title', 'parent_id')

    for per in node_permission:  # {'id', 'title', 'parent_id'}
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)
    return render(
        request,
        'distribute_power.html',
        {
            'user_list': user_list,  # 所有的用户
            'role_list': role_list,  # 所有的角色
            'user_has_roles_dict': user_has_roles_dict,  # 当前用户所拥有的角色
            'role_has_permissions_dict': role_has_permissions_dict,  # 某一个角色所拥有的权限   某一个用户所拥有的所有的权限
            'all_menu_list': all_menu_list,  # 所有的菜单信息 父权限 子权限  普通的权限
            'uid': uid,
            'rid': rid
        }
    )

