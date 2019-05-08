from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views import View
from crm import models
from crm.forms import RegForm
import hashlib
from rbac.server import init_permission

class Login(View):
    def get(self,request):
        return render(request,"new_login.html",{'error':''})
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        obj=models.UserProfile.objects.filter(username=username,password=password,is_active=True)[0]
        if obj:
            permission=init_permission.InitPermission(obj,request)
            permission.per_init()
            request.session['pk']=obj.pk
            # return redirect('index')
            return redirect(reverse('public_customer'))
        else:
            return render(request,"new_login.html",{'error':'用户名或密码错误'})


class Reg(View):
    def get(self,request):
        form_obj=RegForm()
        context={}
        context['form_obj']=form_obj
        return render(request,"new_register.html",context)
    def post(self,request):
        form_obj=RegForm(request.POST)
        if form_obj.is_valid():
            #二选一，上面是自定义保存的，下面是自己保存自动踢出多余数据
            # form_obj.cleaned_data.pop('re_password')
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect('/crm/login/')
        print(form_obj.errors)
        return render(request, "new_register.html", {"form_obj":form_obj})

class Index(View):
    def get(self,request):
        cur_user=request.session['cur_user']
        return render(request,'index.html',{'cur_user':cur_user})