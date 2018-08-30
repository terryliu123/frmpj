from django.shortcuts import render,HttpResponse
from django.db.models import Count,Q
import re,json
from datetime import datetime
from UserMGR import models,Common,Sysforms

# 用户登陆操作
def login(request):
    if request.method == 'GET' :
        return render(request, "login.html",{'error_msg':''})
    elif request.method=='POST' :
        # 菜单加载
        uname=request.POST.get('username','guest')
        pword=request.POST.get('password','0')
        lis = models.UserInfo.objects.filter(username=uname,password=pword).values('id','username','person__org_id', 'password','person__pstate','role_id','person_id')
        if len(lis)>0 :
            if str(lis[0]['person__pstate']) == '1':
                return render(request, "login.html", {'error_msg': '该用户已停用！'})
            # 用户名
            request.session["username"] =str(lis[0]['username'])
            # 用户ID
            request.session["user_id"] = str(lis[0]['id'])
            # 角色ID
            request.session["role_id"] = str(lis[0]['role_id'])
            # 组织架构ID
            # 人员基本信息ID
            request.session["person_id"] = str(lis[0]['person_id'])
            menulist = Common.rolemenu(request.session["role_id"])
            return render(request, "index.html", {'menulist': menulist,'username':uname})
        else :
            return render(request,"login.html",{'error_msg':'用户名密码错误！'})
    else :
        return render(request, "login.html", {'error_msg': '用户名密码错误！'})
# 主页面
@Common.user_session_filter
def index(request):
#菜单加载
    menulist = Common.rolemenu(request.session['role_id'])
    return render(request, "index.html", {'menulist': menulist,'username':request.session.get("username")})
# Welcome
def welcome(request):
    Common.rolemenu(1)
    return render(request,"welcome.html")
# 组织结构管理
def orglist(request):
    return render(request, "org-tree.html")
# 组织架构操作，增加、删除、修改、移动、加载
def orgec(request,ectype):
    orgid = request.POST.get('orgid')
    text=request.POST.get('text')
    pos=request.POST.get('pos')
    parent=request.POST.get('parent')
    if ectype == 'add':
        obj = models.OrgInfo.objects.create(parent=parent, text=text, orderid=pos)
        orgid=obj.id
    elif ectype == 'modify':
        models.OrgInfo.objects.filter(id=int(orgid)).update(parent=parent, text=pos)
    elif ectype == 'move':
        models.OrgInfo.objects.filter(id=int(orgid)).update(parent=parent, text=text, orderid=pos)
    elif ectype =='delete':
        models.OrgInfo.objects.filter(id=int(orgid)).delete()
    elif ectype == 'load':
        org = models.OrgInfo.objects.all().values("id", "parent", "text")
        lis = list(org)
        return HttpResponse(json.dumps(lis), content_type="application/json")
    return HttpResponse(json.dumps(orgid), content_type="application/json")

# 角色列表
def rolelist(request):
    obj = models.RoleInfo.objects.all().values()
    return render(request,'')

# 人员列表
def personpage(request):
    return render(request,'person-list.html',{'plist':""})
def personlist(request):
    page=int(request.GET.get("page")) # 页码的参数名称，默认：page
    limit=int(request.GET.get("limit")) # 每页数据量的参数名，默认：limit
    org = request.GET.get("org",'')
    name = request.GET.get("pname",'')
    tel = request.GET.get("ptel",'')
    address = request.GET.get("paddress",'')
    nums = page*limit
    obj = list(models.PersonInfo.objects.filter(Q(pname__startswith=name),Q(ptel__startswith=tel),Q(paddress__startswith=address),Q(org__text__startswith=org))
               .values("id","userinfo__id","userinfo__username",
                                                 "pname","org__text","psex","paddress","pbirthdays","pdate",
                                                 "pemail","ptel","pstate","userinfo__role__rolename"))[nums-limit:nums]
    lenl=models.PersonInfo.objects.filter(Q(pname__startswith=name),Q(ptel__startswith=tel),Q(paddress__startswith=address),Q(org__text__startswith=org)).aggregate(c=Count('id'))

    # code: 200  成功的状态码  # msg  状态信息的字段名称  # count 数据总数的字段名称  # data 数据列表的字段名称
    for l in obj :
        l['pbirthdays']=l['pbirthdays'].strftime('%Y-%m-%d')
        if l['psex']==0 :
            l['psex'] = '男'
        else :
            l['psex'] = '女'
        if l['pstate'] == 0 :
            l['pstate'] = "启用"
        else:
            l['pstate'] = "停用"
        l['pdate'] = l['pdate'].strftime('%Y-%m-%d %H:%M:%S')

    reponse_data={'code':0,'msg':'','count':lenl['c'],"data":obj}
    return HttpResponse(json.dumps(reponse_data), content_type="application/json")
# 详细页面
def persondetail(request,ectype,pid):
    if ectype == 'mod':
        obj = models.PersonInfo.objects.filter(id=pid).values("id","userinfo__id","userinfo__username","userinfo__role_id","pname","org_id","org__text","psex","pbirthdays","paddress","pemail","ptel","pdate","pstate","note").first()
        obj['orglist']=models.OrgInfo.objects.all().values('id','text','parent')
        obj['rolelist'] = models.RoleInfo.objects.all().values('id', 'rolename')
        return render(request, 'person-mod.html', {'obj': obj})
    elif ectype == 'add':
        obj=models.OrgInfo.objects.all().values('id','text','parent')
        rolel = models.RoleInfo.objects.all().values('id', 'rolename')
        return render(request, 'person-add.html', {'obj': obj,'rolel':rolel})
    return render(request,"person-add.html",{'orglist':orglist})
# 新增、修改内容
# @transaction.atomic
def person(request,ectype,pid,state):
    try:
        #修改个人信息
        if ectype == 'mod' :
             form = Sysforms.Personform(request.GET)
             models.UserInfo.objects.filter(id=form.data['userid']).update(username=form.data['username'],role_id=form.data['roleid'])
             models.PersonInfo.objects.filter(id=pid).update(pname=form.data['pname'],psex=form.data['psex'],pemail=form.data['pemail'],
                                                        org_id=form.data['org'],ptel=form.data['ptel'],paddress=form.data['paddress'],
                                                        pstate=form.data['pstate'],note=form.data['note'],pbirthdays=form.data['pbirthdays'], pdate=datetime.now())
        #      增加个人信息
        elif ectype == 'add':
            form = Sysforms.Personform(request.GET)
            obj = models.PersonInfo.objects.create(pname=form.data['pname'], psex=form.data['psex'],pemail=form.data['pemail'],
                                                        org_id=form.data['org'], ptel=form.data['ptel'],paddress=form.data['paddress'],
                                                        pstate=form.data['pstate'], note=form.data['note'],pbirthdays=datetime.strptime(form.data['pbirthdays'],"%Y-%m-%d"),
                                                        pdate=datetime.now())
            #增加个人信息时间默认创建个用户，默认密码111111
            models.UserInfo.objects.create(username=form.data['username'],password="111111",role_id=form.data['roleid'],person_id=obj.id)
            #删除个人信息
        elif ectype == 'del':
            p1 = models.PersonInfo.objects.get(id=pid)
            p1.userinfo_set.clear()
            p1.delete()
            #删除所有
        elif ectype == 'delall':
            pa= re.split(',',pid)
            for i in pa :
                p1 = models.PersonInfo.objects.get(id=i)
                p1.userinfo_set.clear()
                p1.delete()
        #修改账户状态，启用或停用
        elif ectype == 'start' :
                models.PersonInfo.objects.filter(id=pid).update(pstate=state)
        return HttpResponse(json.dumps('suc'), content_type="application/json")
    except BaseException:
        return HttpResponse(json.dumps('false'), content_type="application/json")
#检测用户是否在数据库中有同名
def checkuser(request,username):
    obj = models.UserInfo.objects.filter(username=username).values('id');
    if len(obj)>0 :
        return HttpResponse(json.dumps('1'), content_type="application/json")
    return HttpResponse(json.dumps('0'), content_type="application/json")
#检测用户是否在数据库中有同名
def modcheckuser(request,f,s):

    obj = models.UserInfo.objects.filter(username=f).values('id');
    if len(obj)>0 :
        return HttpResponse(json.dumps('1'), content_type="application/json")
    return HttpResponse(json.dumps('0'), content_type="application/json")
# 修改密码
def modpwd(request,ectype,pid):
    if ectype == 'detail':
        obj = models.UserInfo.objects.filter(person_id=pid).values("username","id").first()
        return render(request,"user-pwd.html",{"obj":obj})
    elif ectype == 'mod' :
        models.UserInfo.objects.filter(person_id=pid).update(password=request.GET.get("password"))
    return HttpResponse(json.dumps('suc'), content_type="application/json")
