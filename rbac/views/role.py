from django.shortcuts import render,redirect
from rbac import models
from rbac.form import RoleForm

def role_list(request):
    """
    客户列表
    :return:
    """
    data_list = models.Role.objects.all()

    return render(request, 'role_list.html', {'data_list': data_list})

def role_add(request):
    """
    新增
    :return:
    """
    if request.method == 'GET':
        form = RoleForm()
        return render(request, 'add_role.html', {'form': form})
    form = RoleForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('rbac:show_role')
    return render(request, 'add_role.html', {'form': form})

def role_edit(request, rid):
    """
    编辑
    :return:
    """
    obj = models.Role.objects.get(id=rid)
    if request.method == 'GET':
        form = RoleForm(instance=obj)
        return render(request, 'add_role.html', {'form': form})
    form = RoleForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('rbac:show_role')
    return render(request, 'add_role.html', {'form': form})

def role_del(request, rid):
    """
    删除角色
    :param request:
    :param cid:
    :return:
    """
    models.Role.objects.filter(id=rid).delete()
    return redirect('rbac:show_role')