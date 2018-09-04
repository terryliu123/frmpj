from django import  forms
from SysMGR import models
from django.forms import widgets

class Personform(forms.Form):
    org = forms.CharField(label='所属部门')
    pname = forms.CharField(label='姓名')
    psex = forms.fields.CharField(label='性别',
        initial=2, widget=widgets.Select(choices=((0,'男'),1,'女 '),))
    pbirthdays = forms.DateField(label='出生日期')
    ptel = forms.CharField(label='电话')
    pemail = forms.CharField(label='邮箱')
    paddress = forms.CharField(label='地址')
    pstate = forms.IntegerField(label='状态')
    pdate = forms.DateTimeField(label='创建时间')
    note = forms.CharField(label='简介')
    username=forms.CharField()
    userid = forms.CharField()
    roleid = forms.CharField()
