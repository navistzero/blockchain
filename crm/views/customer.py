from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views import View
from crm import models
from crm.forms import CustomerForm,ConsultForm,EnrollmentForm
from crm.pagenation import Pagenation
from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.contrib import messages

class Customer(View):
    def get(self,request):
        all_cus=models.Customer.objects.all()
        context = {}
        context['all_cus'] = all_cus
        return render(request,'customer.html',context)

# class AddCustomer(View):
#     def get(self,request):
#         customer_obj = CustomerForm()
#         return render(request,'add_customer.html',{'customer_obj':customer_obj})
#     def post(self,request):
#         customer_obj = CustomerForm(request.POST)
#         if customer_obj.is_valid():
#             customer_obj.save()
#             return redirect(reverse('public_customer'))
#         return render(request, 'customer.html', {'customer_obj': customer_obj})
#
# class EditCustomer(View):
#     def get(self,request,edit_id):
#         change_obj=models.Customer.objects.filter(pk=edit_id)[0]
#         form_obj = CustomerForm(instance=change_obj)
#         return render(request,'add_customer.html',{'customer_obj':form_obj})
#     def post(self,request,edit_id):
#         change_obj = models.Customer.objects.filter(pk=edit_id)[0]
#         customer_obj = CustomerForm(request.POST, instance=change_obj)
#         if customer_obj.is_valid():
#             customer_obj.save()
#             return redirect(reverse('public_customer'))
#         return render(request, 'add_customer.html', {'customer_obj': customer_obj})

class CustomerChange(View):
    def get(self,request,edit_id=None):
        change_obj = models.Customer.objects.filter(pk=edit_id).first()
        form_obj = CustomerForm(instance=change_obj)
        return render(request, 'add_customer.html', {'customer_obj': form_obj})
    def post(self,request,edit_id=None):
        change_obj = models.Customer.objects.filter(pk=edit_id).first()
        customer_obj = CustomerForm(request.POST, instance=change_obj)
        if customer_obj.is_valid():
            customer_obj.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
            # return redirect(reverse('public_customer'))
        title = '编辑客户' if edit_id else '添加客户'
        return render(request, 'add_customer.html', {'customer_obj': customer_obj,'title': title})

class CustomerList(View):

    def search(self,filter_list):
        querry=self.request.GET.get('querry','')
        q=Q()
        for i in filter_list:
            q.children.append(Q(('{}__contains'.format(i),querry)))
        # children=[Q({}}__contains=querry),
        q.connector='OR'
        return q

    def get(self,request):
        q=self.search(['qq','name'])
        query_dict=request.GET.copy()
        url_dict={
            reverse('public_customer'):1,
            reverse('private_customer'):0,
        }
        if url_dict[request.path_info]:
            customer_obj=models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            customer_obj = models.Customer.objects.filter(q,consultant__pk=request.session['pk'])
        # page = Pagenation(customer_obj, request.GET.get('page', 1), 5, 2, querry_dict)
        page = Pagenation(customer_obj, 5, 2, query_dict)
        context = {'date':page.current_page_show_data,
        'pagenation_html':page.navgation,}
        # context['all_cus'] = customer_obj
        return render(request, 'customer.html', context)

    def post(self,request):
        opreation=request.POST.get('batch')
        if hasattr(self,opreation):
            cur_user_pk=request.session['pk']
            ret=getattr(self,opreation)(cur_user_pk)
            if ret:
                messages.success(request,ret)
                return redirect(reverse('public_customer'))
            else:
                return redirect(reverse('private_customer'))
        else:
            return HttpResponse('error')


    def pub_to_pri(self,pk):
        tips=''
        ids = self.request.POST.getlist('ids')
        # 方式一
        private_customer_num=len(ids)+models.Customer.objects.filter(consultant_id=pk).count()
        if private_customer_num>settings.MAX_CUSTOMER:
            tips="已超过规定选择人数，无法执行！"
            return tips
        else:
            try:
                with transaction.atomic():
                    querry_set=models.Customer.objects.filter(pk__in=ids,consultant__isnull=True).select_for_update()
                    if len(ids)==querry_set.count():
                        querry_set.update(consultant_id=pk)
                    else:
                        tips='该客户已经不存在或者已经不是公共客户'
                    return tips
            except Exception:
                pass
        # 方式二
        # self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=ids))

    def pri_to_pub(self,pk):
        tips=''
        ids = self.request.POST.getlist('ids')
        # 方式一
        models.Customer.objects.filter(pk__in=ids).update(consultant_id=None)
        # 方式二
        # self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=ids))
        return tips

class ConsultList(View):
    def search(self,filter_list):
        querry=self.request.GET.get('querry','')
        q=Q()
        for i in filter_list:
            q.children.append(Q(('{}__contains'.format(i),querry)))
        # children=[Q({}}__contains=querry),
        q.connector='OR'
        return q

    def get(self,request,customer_id=None):
        q=self.search([])
        query_dict=request.GET.copy()
        if customer_id:
            consult_obj=models.ConsultRecord.objects.filter(q,customer_id=customer_id).order_by('-date')
        else:
            consult_obj=models.ConsultRecord.objects.filter(q,consultant_id=request.session['pk']).order_by('-date')
        page = Pagenation(consult_obj, 5, 2, query_dict)
        context = {'date':page.current_page_show_data,
        'pagenation_html':page.navgation,}
        # context['all_cus'] = customer_obj
        return render(request, 'consult.html', context)
        
class AddConsult(View):
    def get(self,request):
        obj = models.ConsultRecord(consultant_id=request.session['pk'])
        consult_obj = ConsultForm(instance=obj)
        title='添加纪录'
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})
    def post(self,request):
        obj = models.ConsultRecord(consultant_id=request.session['pk'])
        consult_obj=ConsultForm(request.POST,instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            return redirect(reverse('consult_record'))
        title='添加纪录'
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})

class EditConsult(View):
    def get(self,request,edit_id):
        # query_dict=request.GET.copy()
        obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
        consult_obj = ConsultForm(instance=obj)
        title='编辑纪录'
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})
    def post(self,request,edit_id):
        obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
        consult_obj=ConsultForm(request.POST,instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
        title='编辑纪录'
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})

class ChangeConsult(View):
    def get(self,request,edit_id=None):
        # query_dict=request.GET.copy()
        if edit_id:
            obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
            title='编辑纪录' 
        else:
            obj = models.ConsultRecord(consultant_id=request.session['pk'])
            title='添加纪录'
        consult_obj = ConsultForm(instance=obj)
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})
    def post(self,request,edit_id=None):
        obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
        consult_obj=ConsultForm(request.POST,instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
        title='编辑纪录' if edit_id else '添加纪录'
        return render(request, 'form.html', {'form_obj': consult_obj,'title': title})


class Enrollment(View):
    def search(self,filter_list):
        querry=self.request.GET.get('querry','')
        q=Q()
        for i in filter_list:
            q.children.append(Q(('{}__contains'.format(i),querry)))
        # children=[Q({}}__contains=querry),
        q.connector='OR'
        return q

    def get(self,request):
        q=self.search([])
        query_dict=request.GET.copy()
        enrollment_obj=models.Enrollment.objects.filter(q,customer__consultant_id=request.session['pk'])
        page = Pagenation(enrollment_obj, 5, 2, query_dict)
        context = {'date':page.current_page_show_data,
        'pagenation_html':page.navgation,}
        # context['all_cus'] = customer_obj
        return render(request, 'enrollment.html', context)

class EnrollmentChange(View):
    def get(self,request,customer_id=None,edit_id=None):
        if customer_id:
            obj=models.Enrollment(customer_id=customer_id)
        else:
            obj=models.Enrollment.objects.filter(pk=edit_id).first()
        erollment_obj=EnrollmentForm(instance=obj)
        title='添加报名表' if customer_id else '编辑报名表'
        return render(request,'form.html',{'form_obj': erollment_obj,'title': title})
    def post(self,request,customer_id=None,edit_id=None):
        obj=models.Enrollment.objects.filter(pk=edit_id).first()
        enrollment_obj=EnrollmentForm(request.POST,instance=obj)
        if enrollment_obj.is_valid():
            enrollment_obj.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
        title='编辑报名表'
        return render(request, 'form.html', {'form_obj': enrollment_obj,'title': title})
