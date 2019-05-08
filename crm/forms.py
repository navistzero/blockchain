from crm import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import hashlib

class BootStrapModelform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			if isinstance(field, (forms.MultipleChoiceField, forms.BooleanField)):
				continue
			field.widget.attrs['class'] = 'form-control'

class RegForm(forms.ModelForm):
    username = forms.EmailField(
        max_length=32,
        required=True,
        label="user_name",
        widget=forms.EmailInput(attrs={
            'placeholder': '请填写邮箱',
            'class':"inputstyle2"
        }),
        error_messages={'required': '这个框框必须填哦',}
    )
    password=forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':'填写密码','class':"inputstyle2"}),
        )
    re_password=forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':'确认密码','class':"inputstyle2"})
    )
    name=forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '您的真实姓名','class':"inputstyle2"}),
    )
    mobile=forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '填写手机号', 'class': "inputstyle2"}),
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请填写正确的手机号码')]
    )

    class Meta:
        model=models.UserProfile
        fields='__all__'
        exclude=['is_active']
        widgets={
            # 'name': forms.TextInput(attrs={'placeholder': '您的真实姓名'}),
            # 'username': forms.EmailInput(attrs={'placeholder':'您的用户名'},),
            # 'password': forms.PasswordInput(attrs={'placeholder': '输入密码'}),
            # 'mobile': forms.TextInput(attrs={'placeholder': '您的手机号'}),
        }

    #     error_message={
    #         'username':{'invalid':'请输入正确的邮箱地址'}
    #     }
    #
    def clean_re_password(self):
        password=self.cleaned_data.get('password')
        re_password=self.cleaned_data.get('re_password')
        if password==re_password and password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            password = md5.hexdigest()
            self.cleaned_data['password']=password
            return self.cleaned_data
        # self.add_error('re_passwprd','两次密码不一致')
        raise ValidationError('两次密码不一致')

class CustomerForm(BootStrapModelform):
    class Meta:
        model=models.Customer
        fields='__all__'


class ConsultForm(BootStrapModelform):
	class Meta:
		model = models.ConsultRecord
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['customer'].choices = [('', '-----------'), ] + [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
		self.fields['consultant'].choices = [(self.instance.consultant_id, self.instance.consultant)]

class EnrollmentForm(BootStrapModelform):
    class Meta:
        model= models.Enrollment
        fields='__all__'
        exclude=['contract_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].choices = [(self.instance.customer_id, self.instance.customer)]

class ClassListForm(BootStrapModelform):
    class Meta:
        model=models.ClassList
        fields='__all__'

class CourseRecordForm(BootStrapModelform):
    class Meta:
        model=models.CourseRecord
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制班级为当前的班级
        self.fields['re_class'].choices = [(self.instance.re_class_id,self.instance.re_class)]
        # 限制记录者为当前的用户
        self.fields['recorder'].choices = [(self.instance.recorder_id,self.instance.recorder)]
        # 限制讲师为当前的班级的老师
        self.fields['teacher'].choices = [ (teacher.pk,str(teacher)) for teacher in self.instance.re_class.teachers.all() ]

class StudyRecordForm(BootStrapModelform):
    class Meta:
        model=models.StudyRecord
        fields='__all__'
