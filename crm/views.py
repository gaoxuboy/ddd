from django.shortcuts import render,redirect
from rbac import models as rbac_models
from rbac.service.rbac import initial_permission


def index(request):
    return render(request,'index.html')


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = rbac_models.User.objects.filter(username=user,password=pwd).first()
        if obj:
            # 用户权限初始化
            initial_permission(request,obj)
            # 跳转到首页
            return redirect('/index/')

        else:
            return render(request, 'login.html')

