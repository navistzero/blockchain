from django.conf.urls import url
from crm.views import auth
from crm.views import customer,teacher

urlpatterns = [
    url(r'^login/$',auth.Login.as_view(),name='login'),
    url(r'^register/$',auth.Reg.as_view(),name='register'),
    url(r'^index/$', auth.Index.as_view(), name='index'),
    # url(r'^show_customer/',customer.Customer.as_view(),name='show_customer'),
    url(r'^add_customer/$',customer.CustomerChange.as_view(),name='add_customer'),
    url(r'^edit_customer/(\d+)$',customer.CustomerChange.as_view(),name='edit_customer'),

    url(r'^public_customer/$',customer.CustomerList.as_view(),name='public_customer'),
    url(r'^private_customer/$',customer.CustomerList.as_view(),name='private_customer'),

    # 展示所有的跟进记录
    url(r'^consult_record/$',customer.ConsultList.as_view(),name='consult_record'),
    # 展示某个客户的跟进记录
    url(r'^consult_record/(\d+)$',customer.ConsultList.as_view(),name='someone_consult'),
    url(r'^add_consult/$',customer.AddConsult.as_view(),name='add_consult'),
    url(r'^edit_consult/(\d+)$',customer.EditConsult.as_view(),name='edit_consult'),
        
    url(r'^enrollment/$',customer.Enrollment.as_view(),name='enrollment'),
    url(r'^add_enrollment/(?P<customer_id>\d+)$',customer.EnrollmentChange.as_view(),name='add_enrollment'),
    url(r'^edit_enrollment/(?P<edit_id>\d+)$',customer.EnrollmentChange.as_view(),name='edit_enrollment'),
        
    url(r'^class_list/$',teacher.ClassList.as_view(),name='class_list'),
    url(r'^add_class_list/$',teacher.ClassListChange.as_view(),name='add_class_list'),
    url(r'^edit_class_list/(?P<edit_id>\d+)$',teacher.ClassListChange.as_view(),name='edit_class_list'),

    url(r'^course_record/(?P<class_id>\d+)$',teacher.CourseRecord.as_view(),name='course_record'),
    url(r'^add_course_record/(?P<class_id>\d+)$',teacher.CourseRecordChange.as_view(),name='add_course_record'),
    url(r'^edit_course_record/(?P<edit_id>\d+)$',teacher.CourseRecordChange.as_view(),name='edit_course_record'),

    url(r'^study_record_list/(?P<course_record_id>\d+)$',teacher.StudyRecordList.as_view(),name='study_record_list'),
]