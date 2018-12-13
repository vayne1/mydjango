from stark.service.stark import site,StarkConfig,SearchOption,Row
from django.conf.urls import re_path
from django.shortcuts import HttpResponse
from cmdb import models



class RoleConfig(StarkConfig):
    list_display = [
        StarkConfig.display_checkbox,
        'instance_name',
        'area',
        'outside_ip',
        'cloud',
        StarkConfig.display_edit_del,
        ]
    search_list = [
        'instance_name',
        'area',
        'outside_ip',
        'cloud__type',
    ]
    action_list = []


class DistinctNameOption(SearchOption):

    def get_queryset(self, _field, model_class, query_dict):

        return Row(model_class.objects.filter(**self.condition).values_list('title').distinct(),self,query_dict)


class BookConfig(StarkConfig):
    list_display = [StarkConfig.display_checkbox, 'title','price','user',StarkConfig.display_edit_del]

    def test(self,request):
        return HttpResponse('test')
    test.text = 'test'
    action_list = [test,]
    search_list = ['title','price','user__title']
    list_filter = [
        DistinctNameOption('title',text_func=lambda x:x[0],value_func=lambda x:x[0]),
        SearchOption('level',is_choice=True,text_func=lambda x:x[1],is_multi=True),
        SearchOption('user_id',text_func=lambda x:x.user.title,value_func=lambda x:x.user_id),
    ]

site.register(models.host,RoleConfig)