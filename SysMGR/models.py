from django.db import models

# 角色基本信息表
class RoleInfo(models.Model):
    rolename = models.CharField(max_length=32)
    note = models.CharField(max_length=64, default='', null=True)
#组织架构基本信息表
class OrgInfo(models.Model):
    text = models.CharField(max_length=32,verbose_name='部门名称')
    parent=models.CharField(max_length=32,verbose_name='父项ID')
    orderid=models.IntegerField(default=0,verbose_name='顺序')
    note = models.CharField(max_length=64,default='',verbose_name='备注',null=True)
# 人员基本信息表
class PersonInfo(models.Model):
    org = models.ForeignKey(OrgInfo, on_delete=models.CASCADE, to_field='id', default='',verbose_name='所属部门')
    pname = models.CharField(max_length=32,verbose_name='姓名',null=True)
    psex=models.IntegerField(default=0,null=True)
    pbirthdays=models.DateField(blank=True,verbose_name='出生日期',null=True)
    ptel= models.CharField(max_length=32,default='',verbose_name='电话',null=True)
    # pduty=models.CharField(max_length=32,default='',verbose_name='职务',null=True)
    pemail= models.CharField(max_length=32,default='',verbose_name='邮箱地址',null=True)
    paddress=models.CharField(max_length=32,default='',verbose_name='地址',null=True)
    pstate =models.IntegerField(default=0,verbose_name='状态',null=True)
    pdate=models.DateTimeField(blank=True,verbose_name='创建时间',null=True)
    note = models.CharField(max_length=64,default='',verbose_name='备注',null=True)

class UserInfo(models.Model):
    username = models.CharField(max_length=32, null=True)
    password = models.CharField(max_length=64, null=True)
    role = models.ForeignKey(RoleInfo, on_delete=models.CASCADE, to_field='id', default='',
                             null=True)  # 表中生成列名：role_id
    person = models.ForeignKey(PersonInfo, on_delete=models.CASCADE, to_field='id', default='', null=True)
# 菜单基本信息表
class MenuInfo(models.Model):
    text = models.CharField(max_length=32,null=True)
    url = models.CharField(max_length=64,null=True)
    level=models.IntegerField(default=0,null=True)
    parent = models.CharField(max_length=32,null=True)
    orderid=models.IntegerField(default=100,null=True)
    note = models.CharField(max_length=64,default='',null=True)
# 角色菜单权限表
class RolemenuInfo(models.Model):
    role = models.ForeignKey(RoleInfo, on_delete=models.CASCADE, to_field='id', default='', null=True)
    menu = models.ForeignKey(MenuInfo, on_delete=models.CASCADE, to_field='id', default='', null=True)
    note = models.CharField(max_length=64, default='', null=True)