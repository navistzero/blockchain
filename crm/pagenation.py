from django.shortcuts import render,HttpResponse,redirect
from django.http.request import QueryDict

# user_list=['name{}'.format(i) for i in range(305)]

class Pagenation():
    def __init__(self,datalist,max_pagenation_show=5,max_page_data_show=10,query_dict=None):
        """
        :param datalist: 要显示的数据列表
        :param current_page: 当前页数
        :param max_pagenation_show: 分页栏展示个数
        :param max_page_data_show: 每页最多展示数据个数
        """
        self.datalist=datalist
        try:
            self.current_page=int(query_dict.get('page',1))
        except Exception:
            self.current_page=1
        self.max_pagenation_show=max_pagenation_show
        self.max_page_data_show=max_page_data_show
        self.query_dict=query_dict if query_dict else QueryDict(mutable=True)

    def page_count(self):
        # 返回总页数
        a, b = divmod(len(self.datalist), self.max_page_data_show)
        if not a:
            page_count = 1
        else:
            if (b):
                page_count = len(self.datalist) // self.max_page_data_show + 1
            else:
                page_count = len(self.datalist) // self.max_page_data_show
        return page_count

    @property
    def cur_page(self):
        cur_page=self.current_page
        if cur_page<1:
            cur_page=1
        elif cur_page>self.page_count():
            cur_page=self.page_count()
        return cur_page

    @property
    def current_page_show_data(self):
        '''
        :return:返回 当前页数展示数据开头和结尾id
        '''
        # 当前页数展示数据开头和结尾id
        cur_page_start = (self.cur_page - 1) * self.max_page_data_show
        cur_page_end = self.cur_page * self.max_page_data_show
        return self.datalist[cur_page_start:cur_page_end]

    @property
    def navgation(self):
        '''
        :return:
        '''
        ret=[]
        page_count=self.page_count()   #得到总的页数
        # 返回上一页功能
        if self.cur_page==1:
            ret.append('<li class="disabled"><a aria-label="Previous"><span>&laquo;</span></a></li>')
        else:
            self.query_dict['page']=self.cur_page-1
            ret.append('<li><a href="?{}" aria-label="Previous"><span>&laquo;</span></a></li>'.format(self.query_dict.urlencode()))
        # 中间页码显示
        half_num = self.max_pagenation_show // 2
        left_pagenation = self.cur_page - half_num
        if left_pagenation < 1:
            left_pagenation = 1
        right_pagenation = self.cur_page + half_num + 1
        if right_pagenation > page_count + 1:
            right_pagenation = page_count + 1
        for i in range(left_pagenation,right_pagenation):
            self.query_dict['page']=i
            if i == self.cur_page:
                ret.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i))
            else:
                ret.append('<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i))
        # 跳转到下一页功能
        if self.cur_page==page_count:
            ret.append('<li class="disabled"><a aria-label="Next"><span>&raquo;</span> </a></li>')
        else:
            self.query_dict['page']=self.cur_page+1
            ret.append('<li><a href="?{}" aria-label="Next"><span>&raquo;</span> </a></li>'.format(self.query_dict.urlencode()))
        pagenavigation=''.join(ret)
        return pagenavigation


# def pagenation(request):

#     page=Pagenation(user_list,request.GET.get('page',1),7,10)

#     return render(request,'pagenation.html',{
#         'user':page.current_page_show_data,
#         'pagenation_html':page.navgation,
#         # 'current_page':page.cur_page,
#     })