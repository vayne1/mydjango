from django.shortcuts import render,HttpResponse,redirect
from cmdb import models
from django import forms
from django.forms import widgets,fields
# Create your views here.
import json



def auth(func):
    def inner(request,*args,**kwargs):
        v = request.session.get('username')
        if not v:
            return redirect('/cmdb/login')
        return func(request,*args,**kwargs)
    return inner


def login(request):
    #如果有sessionID就跳转到host页面（功能）
    if request.method == 'GET':
        return render(request,'login.html')

    elif request.method == 'POST':
        user = request.POST.get('value_1')
        pwd = request.POST.get('value_2')
        checkbox = request.POST.get('check')
        username = models.account.objects.filter(username=user).values()
        for i in username:

            if user == i['username'] and pwd == i['password']:
                request.session['username'] = user
                # request.session.clear_expired()
                # request.session.delete("session_key")
                # request.session.clear()
                # res = redirect('/cmdb/host/')
                # res.set_cookie('username',user,max_age=10)
                # return res
                if checkbox:
                    request.session.set_expiry(604800)
                return redirect('/cmdb/host/')
        else:
            print(1)
            return render(request,'login.html')
@auth
def host(request):

    # with open('aa','r',encoding='UTF-8') as f:
    #     n=0
    #     for line in f:
    #         n += 1
    #         all_list = line.strip().split('|')
    #         print(all_list)
    #         models.host.objects.create(
    #             id = n,
    #             instance_name = all_list[0],
    #             area = all_list[1],
    #             outside_ip = all_list[2],
    #             inside_ip = all_list[3],
    #             system = all_list[4],
    #             cpu_num = all_list[5],
    #             ram = all_list[6],
    #             bandwidth = all_list[7],
    #             risk = all_list[8],
    #             cloud_id = all_list[9],
    #             user = all_list[10],
    #         )
    if request.method == 'GET':

        all_info = models.host.objects.all()
        project_name = models.project.objects.all()
        return render(request, 'host.html', {'all_info': all_info, 'project_name': project_name})
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

        return redirect('/cmdb/host/')

@auth
def detail(request,nid):
    if request.method == 'GET':
        project_name = models.project.objects.all()
        alone_info = models.host.objects.filter(id=nid)
        user_soft = models.host.objects.filter(id=nid).values('user','soft')

        for i in user_soft:
            if i['user']:
                # user = json.loads(i['user'])
                user = i['user'].split()
            else:
                user = ''
            if i['soft']:
                soft = i['soft'].split()
            else:
                soft = ''
        return render(request,'detail.html',{'project_name':project_name,'alone_info':alone_info,'user':user,'soft':soft})

    elif request.method == 'POST':
        if request.POST.get('delete'):
            delete_id = request.POST.get('num')
            models.host.objects.filter(id=delete_id).delete()
            return HttpResponse('delete')
        else:
            update_info = request.POST
            update_id = request.POST.get('update_id')
            print(update_id)
            models.host.objects.filter(id=update_id).update(
                                instance_name = update_info['instance_name'],
                                area = update_info['area'],
                                outside_ip = update_info['outer_ip'],
                                inside_ip = update_info['inter_ip'],
                                system = update_info['system'],
                                cpu_num = update_info['cpu'],
                                ram = update_info['ram'],
                                bandwidth = update_info['band'],
                                risk = update_info['risk'],
                                cloud_id=update_info['c_id'],
                                user=update_info['user'],
                                soft=update_info['soft'],
                                )
            return redirect('/cmdb/host/detail-{}.html'.format(update_id))

class account_form(forms.Form):
    status = fields.CharField()
    species = fields.CharField(error_messages={'required':'不能为空'})
    acc_mum = fields.CharField(error_messages={'required':'不能为空'})
    pwd = fields.CharField(error_messages={'required':'不能为空'})


@auth
def account(request):
    if request.method == 'GET':
        all_account = models.all_account.objects.all()
        return render(request,'account_number.html',{'all_account':all_account})
    if request.method == 'POST':
        if request.POST.get('status') == 'add':
            obj = account_form(request.POST)
            res = obj.is_valid()
            print(res)
            if res:
                data = obj.cleaned_data
                models.all_account.objects.create(
                    species = data['species'],
                    acc_mum = data['acc_mum'],
                    pwd = data['pwd']
                )
                print(data)
                response = json.dumps()
                return HttpResponse('add')
            else:
                error = json.dumps(obj.errors)
                return HttpResponse(error)




