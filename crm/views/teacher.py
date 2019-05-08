from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views import View
from crm import models
from crm.forms import ClassListForm,CourseRecordForm,StudyRecordForm
from crm.pagenation import Pagenation
from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.contrib import messages

class BaseView(View):
    def search(self,filter_list):
        querry=self.request.GET.get('querry','')
        q=Q()
        for i in filter_list:
            q.children.append(Q(('{}__contains'.format(i),querry)))
        # children=[Q({}}__contains=querry),
        q.connector='OR'
        return q

class ClassList(BaseView):

    def get(self,request):
        q=self.search([])
        query_dict=request.GET.copy()
        classlist_obj = models.ClassList.objects.filter(q,)
        page = Pagenation(classlist_obj, 5, 2, query_dict)
        context = {'date':page.current_page_show_data,
        'pagenation_html':page.navgation,}
        return render(request, 'teacher\class_list.html', context)

class ClassListChange(BaseView):
    def get(self,request,edit_id=None):
        class_list_obj=models.ClassList.objects.filter(pk=edit_id).first()
        class_list_form=ClassListForm(instance=class_list_obj)
        title='添加班级' if edit_id else '编辑班级'
        return render(request,'form.html',{'form_obj':class_list_form,'title':title})

    def post(self,request,edit_id=None):
        class_list_obj=models.ClassList.objects.filter(pk=edit_id).first()
        class_list_form=ClassListForm(request.POST,instance=class_list_obj)
        if class_list_form.is_valid():
            class_list_form.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
        title='添加班级' if edit_id else '编辑班级'
        return render(request, 'form.html', {'form_obj': class_list_form,'title': title})

class CourseRecord(BaseView):
    def get(self,request,class_id):
        q=self.search([])
        query_dict=request.GET.copy()
        course_record_obj = models.CourseRecord.objects.filter(q,re_class_id=class_id)
        page = Pagenation(course_record_obj, 5, 2, query_dict)
        context = {'date':page.current_page_show_data,
        'pagenation_html':page.navgation,
        'class_id':class_id}
        return render(request, 'teacher\course_record_list.html', context)
    
    def post(self,request,class_id):
        course_record_ids=request.POST.getlist('ids',[])
        for course_record_id in course_record_ids:
            course_record_obj=models.CourseRecord.objects.filter(pk=course_record_id).first()
            students = course_record_obj.re_class.customer_set.filter(status='studying')
            study_record_list = []
            for student in students:
                if not models.StudyRecord.objects.filter(student=student, course_record_id=course_record_id).exists():
                    study_record_list.append(models.StudyRecord(student=student, course_record_id=course_record_id))

            models.StudyRecord.objects.bulk_create(study_record_list)
        return self.get(request,class_id)


    
class CourseRecordChange(BaseView):
    def get(self,request,class_id=None,edit_id=None):
        if class_id and not edit_id:
            obj=models.CourseRecord(re_class_id=class_id,recorder_id=request.session['pk'])
            title='添加课程记录'
        else:
            obj=models.CourseRecord.objects.filter(pk=edit_id).first()
            title='编辑课程记录'
        courserecord_form=CourseRecordForm(instance=obj)
        return render(request,'form.html',{'form_obj': courserecord_form,'title': title})

    def post(self,request,class_id=None,edit_id=None):
        if class_id and not edit_id:
            obj=models.CourseRecord(re_class_id=class_id,recorder_id=request.session['pk'])
            title='添加课程记录'
        else:
            obj=models.CourseRecord.objects.filter(pk=edit_id).first()
            title='编辑课程记录'
        courserecord_form=CourseRecordForm(request.POST,instance=obj)
        if courserecord_form.is_valid():
            courserecord_form.save()
            need_page=request.GET.get('final')
            return redirect(need_page)
        return render(request,'form.html',{'form_obj': courserecord_form,'title': title})
        
from django.forms import modelformset_factory
from django.contrib import messages

class StudyRecordList(BaseView):
    def get(self,request,course_record_id):
        FormSet=modelformset_factory(models.StudyRecord,form=StudyRecordForm,extra=0)
        formset_obj = FormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
        return render(request, 'teacher\study_record_list.html',{'formset_obj':formset_obj})
    
    def post(self,request,course_record_id):
        FormSet=modelformset_factory(models.StudyRecord,form=StudyRecordForm,extra=0)
        formset_obj = FormSet(data=request.POST)
        if formset_obj.is_valid():
            messages.success(request,'保存成功！')
            formset_obj.save()
        return render(request, 'teacher\study_record_list.html',{'formset_obj':formset_obj})