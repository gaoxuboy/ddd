import json
from django.shortcuts import render,HttpResponse,redirect
from arya.service import sites
from . import models



from django.urls.resolvers import RegexURLPattern
from django.forms import ModelForm
from django.forms import fields
from django.forms import widgets


def get_all_url(patterns,prev,is_first=False, result=[]):
    """
    [
        (ur1,ur1,)
        (ur1,ur1,)
        (ur1,ur1,)
        (ur1,ur1,)
    ]
    :param patterns:
    :param prev:
    :param is_first:
    :param result:
    :return:
    """
    if is_first:
        result.clear()
    for item in patterns:
        v = item._regex.strip("^$")
        if isinstance(item, RegexURLPattern):
            val = prev + v
            result.append((val,val,))
        else:
            get_all_url(item.urlconf_name, prev + v)

    return result


class UserConfig(sites.AryaConfig):
    list_display = ['username','email',]
sites.site.register(models.User,UserConfig)


class RoleConfig(sites.AryaConfig):
    list_display = ['caption',]

sites.site.register(models.Role,RoleConfig)


# ###### Form组件 ######
class PermissionModelForm(ModelForm):
    url = fields.ChoiceField()

    class Meta:
        fields = "__all__"
        model = models.Permission

    def __init__(self,*args,**kwargs):
        super(PermissionModelForm,self).__init__(*args,**kwargs)

        from pro_crm.urls import urlpatterns
        # 只显示未加入权限的URL
        self.fields['url'].choices = get_all_url(urlpatterns,'/',True)
class PermissionConfig(sites.AryaConfig):

    def dabo(self, obj=None, is_header=False):
        if is_header:
            return '其他'
        return obj.caption + "-大波"

    list_display = ['caption','url',dabo,'menu']

    model_form = PermissionModelForm
sites.site.register(models.Permission,PermissionConfig)


sites.site.register(models.Menu)