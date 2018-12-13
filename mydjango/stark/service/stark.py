from django.conf.urls import re_path
from django.shortcuts import HttpResponse, render,redirect
from types import FunctionType
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django.db.models import Q
import functools
from django.http import QueryDict
from stark.utils.pagination import Pagination
from django.db.models.fields.related import ForeignKey,ManyToManyField


class Row(object):
    def __init__(self,data_list,option,query_dict):
        """
        组合搜索显示每一列数据
        :param data_list:元组或queryset
        """
        self.data_list = data_list
        self.option = option
        self.query_dict = query_dict

    def __iter__(self):
        yield '<div class="whole">'

        total_query_dict = self.query_dict.copy()
        total_query_dict._mutable = True

        origin_value_list = self.query_dict.getlist(self.option.field)  # [2,]
        if origin_value_list:
            total_query_dict.pop(self.option.field)
            yield '<a href="?%s">全部</a>' % (total_query_dict.urlencode(),)
        else:
            yield '<a class="active" href="?%s">全部</a>' % (total_query_dict.urlencode(),)

        yield '</div>'
        yield '<div class="others">'

        for item in self.data_list:  # item=(),queryset中的一个对象
            val = self.option.get_value(item)
            text = self.option.get_text(item)

            query_dict = self.query_dict.copy()
            query_dict._mutable = True

            if not self.option.is_multi:  # 单选
                if str(val) in origin_value_list:
                    query_dict.pop(self.option.field)
                    yield '<a class="active" href="?%s">%s</a>' % (query_dict.urlencode(), text)
                else:
                    query_dict[self.option.field] = val
                    yield '<a href="?%s">%s</a>' % (query_dict.urlencode(), text)
            else:  # 多选
                multi_val_list = query_dict.getlist(self.option.field)
                if str(val) in origin_value_list:
                    # 已经选，把自己去掉
                    multi_val_list.remove(str(val))
                    query_dict.setlist(self.option.field, multi_val_list)
                    yield '<a class="active" href="?%s">%s</a>' % (query_dict.urlencode(), text)
                else:
                    multi_val_list.append(val)
                    query_dict.setlist(self.option.field, multi_val_list)
                    yield '<a href="?%s">%s</a>' % (query_dict.urlencode(), text)

        yield '</div>'


class SearchOption(object):
    """
    组合搜索
    """
    def __init__(self,field,condition=None,is_choice=False,text_func=None,value_func=None,is_multi=False):
        self.field = field
        self.is_choice = is_choice
        if not condition:
            condition = {}
        self.condition = condition
        self.text_func = text_func
        self.value_func = value_func
        self.is_multi = is_multi

    def get_queryset(self,_field,model_class,query_dict):
        if isinstance(_field,ForeignKey) or isinstance(_field,ManyToManyField):
            row = Row(model_class.objects.filter(**self.condition),self,query_dict)
        else:
            if self.is_choice:
                row = Row(_field.choices,self,query_dict)
            else:
                row = Row(model_class.objects.filter(**self.condition),self,query_dict)
        return row


    def get_text(self,item):
        if self.text_func:
            return self.text_func(item)
        return str(item)

    def get_value(self, item):
        if self.value_func:
            return self.value_func(item)
        if self.is_choice:
            return item[0]
        return str(item)

class StarkConfig(object):
    order_by = []
    list_display = []
    model_form_class = None
    search_list = []
    list_filter = []


    def multi_delete(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(pk__in=pk_list).delete()
        # return HttpResponse('del')
    multi_delete.text = '批量删除'

    def multi_init(self,request):
        pass
    multi_init.text = '批量初始化'
    action_list = [multi_delete,multi_init]

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.back_condition_key = '_filter'

    def display_checkbox(self,row=None,header=False):
        if header:
            return '选择'
        return  mark_safe("<input type='checkbox' name='pk' value='%s'>" %row.pk)

    def display_edit(self,row=None,header=False):
        if header:
            return '操作'
        return  mark_safe("<a href='%s'><i class='glyphicon glyphicon-edit'></i></a>" %self.reverse_edit_url(row))

    def display_del(self,row=None,header=False):
        if header:
            return '操作'
        # return  mark_safe("<a class='btn btn-danger'>删除</a>")
        return  mark_safe("<a href='%s'><i class='glyphicon glyphicon-trash'></i></a>" %self.reverse_del_url(row))

    def display_edit_del(self,row=None,header=False):
        if header:
            return '操作'
        res = '''
            <a href='%s'><i class='glyphicon glyphicon-edit'></i></a>|
            <a href='%s'><i class='glyphicon glyphicon-trash'></i></a>
            '''%(self.reverse_edit_url(row),self.reverse_del_url(row))
        # return  mark_safe("<a class='btn btn-danger'>删除</a>")
        return  mark_safe(res)

    def get_order_by(self):
        return self.order_by

    def get_list_display(self):
        return self.list_display

    def get_add_btn(self):
        return mark_safe('<a class="btn btn-success" href="%s">添加</a>' %self.reverse_add_url())

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class AddModelForm(forms.ModelForm):
            class Meta:
                model = self.model_class
                fields = '__all__'
        return AddModelForm

    def get_action_list(self):
        val = []
        val.extend(self.action_list)
        return val

    def get_action_dict(self):
        val = {}
        for item in self.action_list:
            val[item.__name__] = item
            return val

    def get_search_list(self):
        val = []
        val.extend(self.search_list)
        return val

    def get_search_condition(self,request):
        search_list = self.get_search_list()
        q = request.GET.get('q', '')
        conn = Q()
        conn.connector = 'OR'
        if q:
            for field in search_list:
                conn.children.append(('%s__contains' % field, q))
        return search_list,q,conn

    def get_list_filter(self):
        val = []
        val.extend(self.list_filter)
        return val

    def get_list_filter_condition(self):
        comb_condition = {}
        for option in self.get_list_filter():
            element = self.request.GET.getlist(option.field)
            if element:
                comb_condition['%s__in' % option.field] = element

        return comb_condition

    def changelist_view(self, request):
        # 批量操作
        if request.method == 'POST':
            action_name = request.POST.get('action')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求！')
            response = getattr(self,action_name)(request)
            if response:
                return response

        action_list = self.get_action_list()
        action_list = [{'name': func.__name__, 'text': func.text} for func in action_list]


        #处理搜索
        search_list, q, conn = self.get_search_condition(request)
        #处理分页
        total_count = self.model_class.objects.filter(conn).count()
        query_params = request.GET.copy()
        query_params._mutable = True
        page = Pagination(request.GET.get('page'),total_count,request.path_info,query_params,per_page=10)


        query_set = self.model_class.objects.filter(conn).filter(**self.get_list_filter_condition()).order_by(*self.get_order_by()).distinct()[page.start:page.end]


        list_display = self.get_list_display()
        #添加按钮
        add_btn = self.get_add_btn()

        #组合搜索
        list_filter = self.get_list_filter()
        list_filter_rows = []
        for option in list_filter:
            _field = self.model_class._meta.get_field(option.field)
            row = option.get_queryset(_field,self.model_class,request.GET)
            list_filter_rows.append(row)


        header_list = []
        if list_display:
            for name_or_func in list_display:
                if isinstance(name_or_func,FunctionType):
                    verbose_name = name_or_func(self,header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(name_or_func).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)

        body_list = []
        for row in query_set:
            row_list = []
            if not list_display:
                row_list.append(row)
                body_list.append(row_list)
                continue

            for name_or_func in list_display:
                if isinstance(name_or_func, FunctionType):
                    val = name_or_func(self,row=row)
                else:
                    val = getattr(row,name_or_func)
                row_list.append(val)
            body_list.append(row_list)

        return render(request, 'stark/changelist.html',locals())

    def add_view(self, request):
        AddModelForm = self.get_model_form_class()
        form = AddModelForm()
        if request.method == "POST":
            form = AddModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_changelist_url())

        return render(request,'stark/add_data.html',{'form':form})

    def change_view(self, request, pk):
        edit_obj = self.model_class.objects.filter(pk=pk).first()
        if not edit_obj:
            return HttpResponse('数据不存在')
        ModelFormClass = self.get_model_form_class()
        if request.method == 'POST':
            form = ModelFormClass(data=request.POST, instance=edit_obj)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_changelist_url())
        form = ModelFormClass(instance=edit_obj)
        return render(request, 'stark/add_data.html', {'form': form})

    def delete_view(self, request, pk):
        if request.method == "GET":
            cancel_url = self.reverse_changelist_url()
            return render(request,'stark/delete.html',{'cancel_url':cancel_url})
        self.model_class.objects.filter(pk=pk).delete()
        return redirect(self.reverse_changelist_url())

    def wrapper(self,func):
        @functools.wraps(func)
        def inner(request,*args,**kwargs):
            self.request = request
            return func(request,*args,**kwargs)
        return inner


    def get_urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.changelist_view), name='%s_%s_changelist' % info),
            re_path(r'^add/$', self.wrapper(self.add_view), name='%s_%s_add' % info),
            re_path(r'^(?P<pk>\d+)/change/', self.wrapper(self.change_view), name='%s_%s_change' % info),
            re_path(r'^(?P<pk>\d+)/del/', self.wrapper(self.delete_view), name='%s_%s_del' % info),
        ]

        extra = self.extra_url()
        if extra:
            urlpatterns.extend(extra)

        return urlpatterns

    def extra_url(self):
        pass

    def reverse_add_url(self):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_add' % (namespace, app_label, model_name)
        add_url = reverse(name)

        if not self.request.GET:
            return add_url
        param_str = self.request.GET.urlencode()
        new_query_dict = QueryDict(mutable=True)
        new_query_dict[self.back_condition_key] = param_str
        add_url = '%s?%s' %(add_url,new_query_dict.urlencode())
        return add_url

    def reverse_changelist_url(self):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_changelist' %(namespace,app_label,model_name)
        changelist_url = reverse(name)

        origin_condition = self.request.GET.get(self.back_condition_key)
        if not origin_condition:
            return changelist_url
        changelist_url = '%s?%s' %(changelist_url,origin_condition)
        return changelist_url

    def reverse_edit_url(self,row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_change' %(namespace,app_label,model_name)
        edit_url = reverse(name,args=(row.pk,))

        if not self.request.GET:
            return edit_url
        param_str = self.request.GET.urlencode()
        new_query_dict = QueryDict(mutable=True)
        new_query_dict[self.back_condition_key] = param_str
        edit_url = '%s?%s' %(edit_url,new_query_dict.urlencode())
        return edit_url

    def reverse_del_url(self,row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_del' %(namespace,app_label,model_name)
        del_url = reverse(name,args=(row.pk,))

        if not self.request.GET:
            return del_url
        param_str = self.request.GET.urlencode()
        new_query_dict = QueryDict(mutable=True)
        new_query_dict[self.back_condition_key] = param_str
        del_url = '%s?%s' %(del_url,new_query_dict.urlencode())
        return del_url

    @property
    def urls(self):
        return self.get_urls()


class AdminSite(object):
    def __init__(self):
        self._registry = {}
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, stark_config=None):
        # model_class＝models.Role
        # stark_config=None
        if not stark_config:
            stark_config = StarkConfig
        # model_class＝models.Role
        # stark_config=RoleConfig
        self._registry[model_class] = stark_config(model_class, self)
        """
        {
            models.UserInfo: StarkConfig(models.UserInfo), # 封装：model_class=UserInfo，site=site对象
            models.Role: RoleConfig(models.Role)           # 封装：model_class=Role，site=site对象
        }
        """

    def get_urls(self):

        urlpatterns = []
        # urlpatterns.append(url(r'^x1/', self.x1))
        # urlpatterns.append(url(r'^x2/', self.x2))
        # urlpatterns.append(url(r'^x3/', ([
        #                                      url(r'^add/', self.x1),
        #                                      url(r'^change/', self.x1),
        #                                      url(r'^del/', self.x1),
        #                                      url(r'^edit/', self.x1),
        #                                  ],None,None)))
        # urlpatterns.append(re_path('stark/'),)
        for k, v in self._registry.items():
            # k=modes.UserInfo,v=StarkConfig(models.UserInfo), # 封装：model_class=UserInfo，site=site对象
            # k=modes.Role,v=RoleConfig(models.Role)           # 封装：model_class=Role，site=site对象
            app_label = k._meta.app_label
            model_name = k._meta.model_name
            urlpatterns.append(re_path(r'^%s/%s/' % (app_label, model_name,), (v.urls, None, None)))
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


site = AdminSite()
