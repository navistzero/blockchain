from django import template
from django.urls import reverse
from django.http.request import QueryDict

register=template.Library()

@register.simple_tag
def return_url(request,name,*args,**kwargs):
    # 最终要返回的界面，也就是现在点击编辑按钮的界面
    final_url=request.get_full_path()
    # 需要进入的编辑界面
    next_url=reverse(name,args=args,kwargs=kwargs)
    query_dict=QueryDict(mutable=True)
    query_dict['final']=final_url
    middle_url='{0}?{1}'.format(next_url,query_dict.urlencode())
    return middle_url
