from django.shortcuts import render,redirect,HttpResponse
from cmdb import models
from django import forms
from django.forms import widgets,fields

# Create your views here.
import json
class form_verification(forms.Form):
    user = fields.CharField(error_messages={'required':'用户名不能为空'},
                            widget=widgets.Input(attrs={'class':'a1'})
                            )
    pwd = fields.CharField(error_messages={'required':'密码不能为空','min_length':'密码必须大于4'},max_length=12,min_length=4)
    email = fields.EmailField(error_messages={'required':'邮箱不能为空','invalid':'格式错误'})


def test_form(request):

    if request.method == 'GET':
        obj = form_verification()
        return render(request,'test_form.html',{'obj':obj})
    elif request.method == 'POST':
        obj = form_verification(request.POST)
        res = obj.is_valid()  #验证

        if res:
            print(obj.cleaned_data)
        else:
            print(obj.errors.as_json())
            fa=obj.errors
        return render(request,'test_form.html',{'obj':obj})


def ajax_form(request):
    res_dict = {'status':True,'msg':None}
    if request.method == 'POST':
        obj = form_verification(request.POST)
        res = obj.is_valid()  #验证

        if res:
            data = obj.cleaned_data
            data = json.dumps(data)
        else:
            res_dict['status'] = False
            res_dict['msg'] = obj.errors.as_json()
            data = json.dumps(res_dict)
        return HttpResponse(data)


def test_host(request):
    if request.method == 'GET':

        all_info = models.host.objects.all()
        project_name = models.project.objects.all()
        return render(request, 'test_host.html', {'all_info': all_info, 'project_name': project_name})
    elif request.method == 'POST':
        add_info = request.POST
        h = request.POST.get('user')
        s = request.POST.get('soft')
        # textarea = request.POST.get('text')
        models.host.objects.create(
                        instance_name = add_info['instance_name'],
                        area = add_info['area'],
                        outside_ip = add_info['outer_ip'],
                        inside_ip = add_info['inter_ip'],
                        system = add_info['system'],
                        cpu_num = add_info['cpu'],
                        ram = add_info['ram'],
                        bandwidth = add_info['band'],
                        risk = add_info['risk'],
                        cloud_id = add_info['c_id'],
                        user =h,
                        soft = s,
                    )

        return redirect('/testapp/test_host/')