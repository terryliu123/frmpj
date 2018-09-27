from django.shortcuts import render,HttpResponse,redirect
from SysMGR import models,forms
import re,json,os
from datetime import datetime
from django.db.models import Count,Q
import face_recognition,cv2
from AiStore import id_recognition,sl_face
# 用户是否登陆有效性校验
def user_session_filter(func):
    def in_fun(request):
        user_id = request.session.get("user_id")
        if user_id == '' or user_id is None :
            return redirect("/login/")
        return func(request)
    return in_fun

# 主页面
@user_session_filter
def index(request):
#菜单加载
    menulist = rolemenu(request.session['role_id'])
    return render(request, "index.html", {'menulist': menulist,'username':request.session.get("username")})
def test(request):
    return render(request, "test.html")
def main(request):
    return render(request, "main.html")
def orgtree(request):
    return render(request, "orgtree.html")
def rolel(request):
    return render(request, "role-list.html")
def upload(request):
    return render(request, "upload.html")
def facepage(request):
    return render(request, "face-page.html")
def facelogin(request):
    imgfile = request.FILES.get('file')
    img_path = os.path.join('static/images/',imgfile.name+".jpg")    #存储的路径
    print(img_path)
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
    f.close()
    # 读取图片并识别人脸
    name = sl_face.loadface(img_path)
    ret = {'code': False, 'data': img_path, 'name': name}  # 'data': img_path 数据为图片的路径，
    if name!=[] :
        ret = {'code': True, 'data': img_path, 'name': name[0]}  # 'data': img_path 数据为图片的路径，
        lis = models.UserInfo.objects.filter(username= name[0]).values('id', 'username', 'person__org_id',
                                                                                    'password', 'person__pstate',
                                                                                    'role_id', 'person_id')
        if str(lis[0]['person__pstate']) == '1':
            ret = {'code': False, 'data': img_path, 'name': name[0]}  # 'data': img_path 数据为图片的路径，
        # 用户名
        request.session["username"] = str(lis[0]['username'])
        # 用户ID
        request.session["user_id"] = str(lis[0]['id'])
        # 角色ID
        request.session["role_id"] = str(lis[0]['role_id'])
        # 组织架构ID
        # 人员基本信息ID
        request.session["person_id"] = str(lis[0]['person_id'])

    return HttpResponse(json.dumps(ret))    #将数据的路径发送到前端
def findex(request):
    if request.session["user_id"] == "":
        return render(request, "login.html", {'error_msg': '用户名密码错误！'})
    menulist = rolemenu(request.session["role_id"])
    msgcount = models.MessgeInfo.objects.filter(user= request.session["user_id"]).aggregate(c=Count('id'))
    return render(request, "index.html", {'menulist': menulist, 'username':  request.session["username"], "msgcount": msgcount['c']})
def painface(filename):
    # 读取图片并识别人脸
    img = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(img)
    # 调用opencv函数显示图片
    img = cv2.imread(filename)
    # 遍历每个人脸，并标注
    faceNum = len(face_locations)
    for i in range(0, faceNum):
        top = face_locations[i][0]
        right = face_locations[i][1]
        bottom = face_locations[i][2]
        left = face_locations[i][3]
        start = (left, top)
        end = (right, bottom)
        color = (55, 255, 155)
        thickness = 3
        cv2.rectangle(img, start, end, color, thickness)
        font = cv2.FONT_HERSHEY_DUPLEX
        name =id_recognition.checkface(filename)
        cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # 显示识别结果
    cv2.imwrite(filename,img)

def upload_file(request):
    imgfile = request.FILES.get('file')
    import os
    img_path = os.path.join('static/images/',imgfile.name)    #存储的路径
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
    ret = {'code': True , 'data': img_path}  #'data': img_path 数据为图片的路径，
    painface(img_path)
    import json
    return HttpResponse(json.dumps(ret))    #将数据的路径发送到前端

# 菜单列表
def menu(userid):
#菜单加载
    list1 = models.MenuInfo.objects.filter(menulevel=0).values("id","name","parent","level","url","orderid","note").order_by("parent","orderid")
    list2 = models.MenuInfo.objects.filter(menulevel=1).values("id","name", "parent", "level", "url", "orderid","note").order_by("parent","orderid")
    list3 = models.MenuInfo.objects.filter(menulevel=2).values("id","name","parent","level","url","orderid","note").order_by("parent","orderid")
    # 一级菜单，包含二级菜单
    for l1 in list1:
        lisoth=[]
        for l2 in list2 :
            if l1['id']==l2['parent'] :
                lisoth.append(l2)
        l1['childmenu']=lisoth
    #     二级菜单 包含三级菜单
    for l2 in list2:
        lisoth=[]
        for l3 in list3 :
            if l2['id']==l3['parent'] :
                lisoth.append(l3)
        l2['childmenu'] = lisoth

    return list1
# 角色对应菜单
def rolemenu(roleid):
#菜单加载
    # 一级菜单
    list1 =models.RolemenuInfo.objects.filter(role_id=int(roleid),menu__level=0)\
        .values("menu_id","menu__text","menu__parent","menu__level",
                "menu__url","menu__orderid","menu__note").order_by("menu__parent","menu__orderid")
    # 二级菜单
    list2 = models.RolemenuInfo.objects.filter(role_id=int(roleid), menu__level=1) \
        .values("menu_id", "menu__text", "menu__parent", "menu__level",
                "menu__url", "menu__orderid", "menu__note").order_by("menu__parent", "menu__orderid")
    # 三级菜单
    list3 = models.RolemenuInfo.objects.filter(role_id=int(roleid), menu__level=2) \
        .values("menu_id", "menu__text", "menu__parent", "menu__level",
                "menu__url", "menu__orderid", "menu__note").order_by("menu__parent", "menu__orderid")
    # 一级菜单，包含二级菜单
    for l1 in list1:
        lisoth=[]
        for l2 in list2 :
            if str(l1['menu_id'])==l2['menu__parent'] :
                l1['menu__note']='y'
                lisoth.append(l2)
        l1['childmenu']=lisoth
    #     二级菜单 包含三级菜单
    for l2 in list2:
        lisoth=[]
        for l3 in list3 :
            if str(l2['menu_id'])==l3['menu__parent'] :
                l2['menu__note'] = 'y'
                lisoth.append(l3)
        l2['childmenu'] = lisoth
    return list1
# 用户是否登陆有效性校验
def user_session_filter(func):
    def in_fun(request):
        user_id = request.session.get("user_id")
        if user_id == '' or user_id is None :
            return redirect("/login/")
        return func(request)
    return in_fun

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
            menulist = rolemenu(request.session["role_id"])
            msgcount = models.MessgeInfo.objects.filter(user=str(lis[0]['id'])).aggregate(c=Count('id'))
            return render(request, "index.html", {'menulist': menulist,'username':uname,"msgcount":msgcount['c']})
        else :
            return render(request,"login.html",{'error_msg':'用户名密码错误！'})
    else :
        return render(request, "login.html", {'error_msg': '用户名密码错误！'})

# 人员列表
def personpage(request):
    return render(request, 'person-list.html', {'plist': ""})

def personlist(request):
    page = int(request.GET.get("page"))  # 页码的参数名称，默认：page
    limit = int(request.GET.get("limit"))  # 每页数据量的参数名，默认：limit
    org = request.GET.get("org", '')
    name = request.GET.get("pname", '')
    tel = request.GET.get("ptel", '')
    address = request.GET.get("paddress", '')
    nums = page * limit
    obj = list(models.PersonInfo.objects.filter(Q(pname__contains=name), Q(ptel__contains=tel),
                                                Q(paddress__contains=address), Q(org__text__contains=org))
               .values("id", "userinfo__id", "userinfo__username",
                       "pname", "org__text", "psex", "paddress", "pbirthdays", "pdate",
                       "pemail", "ptel", "pstate", "userinfo__role__rolename"))[nums - limit:nums]
    lenl = models.PersonInfo.objects.filter(Q(pname__contains=name), Q(ptel__contains=tel),
                                            Q(paddress__contains=address),
                                            Q(org__text__contains=org)).aggregate(c=Count('id'))

    # code: 200  成功的状态码  # msg  状态信息的字段名称  # count 数据总数的字段名称  # data 数据列表的字段名称
    for l in obj:
        l['pbirthdays'] = l['pbirthdays'].strftime('%Y-%m-%d')
        if l['psex'] == 0:
            l['psex'] = '男'
        else:
            l['psex'] = '女'
        if l['pstate'] == 0:
            l['pstate'] = "启用"
        else:
            l['pstate'] = "停用"
        l['pdate'] = l['pdate'].strftime('%Y-%m-%d %H:%M:%S')

    reponse_data = {'code': 0, 'msg': '', 'count': lenl['c'], "data": obj}
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
    return render(request,"person-add.html",{'orglist':""})
# 新增、修改内容
# @transaction.atomic
def person(request,ectype,pid,state):
    try:
        #修改个人信息
        if ectype == 'mod' :
             form = forms.Personform(request.GET)
             models.UserInfo.objects.filter(id=form.data['userid']).update(username=form.data['username'],role_id=form.data['roleid'])
             models.PersonInfo.objects.filter(id=pid).update(pname=form.data['pname'],psex=form.data['psex'],pemail=form.data['pemail'],
                                                        org_id=form.data['org'],ptel=form.data['ptel'],paddress=form.data['paddress'],
                                                        pstate=form.data['pstate'],note=form.data['note'],pbirthdays=form.data['pbirthdays'], pdate=datetime.now())
        #      增加个人信息
        elif ectype == 'add':
            form = forms.Personform(request.GET)
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
#---------------
def orgload(request):
    lis = list(models.OrgInfo.objects.all().values("id", "parent", "text"))
    return HttpResponse(json.dumps(lis), content_type="application/json")
def orgec(request,ectype):
        orgid = request.POST.get('orgid')
        text = request.POST.get('text')
        pos = request.POST.get('pos')
        parent = request.POST.get('parent')
        if ectype == 'create_node' or ectype == 'copy_node':
            obj = models.OrgInfo.objects.create(parent=parent, text=text, orderid=pos)
            orgid = obj.id
        elif ectype == 'rename_node':
            models.OrgInfo.objects.filter(id=int(orgid)).update(parent=parent, text=pos)
        elif ectype == 'move_node':
            models.OrgInfo.objects.filter(id=int(orgid)).update(parent=parent, text=text, orderid=pos)
        elif ectype == 'delete_node':
            models.OrgInfo.objects.filter(id=int(orgid)).delete()
        return HttpResponse(json.dumps(orgid), content_type="application/json")

def rolelist(request):
    page=int(request.GET.get("page")) # 页码的参数名称，默认：page
    limit=int(request.GET.get("limit")) # 每页数据量的参数名，默认：limit
    name=request.GET.get("powername",'')
    nums = page*limit
    obj = models.RoleInfo.objects.filter(Q(rolename__contains=name)).values("rolename","id","note")[nums-limit:nums]
    lenl = models.RoleInfo.objects.filter(Q(rolename__contains=name)).aggregate(c=Count('id'))
    reponse_data = {'code': 0, 'msg': '', 'count': lenl['c'], "data": list(obj)}
    return HttpResponse(json.dumps(reponse_data), content_type="application/json")

def rolemenulist(request,roleid):
    obj = list(models.MenuInfo.objects.all().values("id","text","parent"))
    rolemenu= list(models.RolemenuInfo.objects.filter(role_id=roleid).values("menu_id"))
    for i in obj:
        i['state']={'opened':False,"selected":False}
        for r in rolemenu :
            if i['id']== r['menu_id'] : #如果菜单中的id存在，那就选中
                i['state']={"opened":True,"selected":True}
            # else : #否则不选中
            #     i['state'] = {"opened": False, "selected": False}
    return HttpResponse(json.dumps(obj), content_type="application/json")

def rolepage(request):
    return render(request, "role-add.html")
def roleadd(request):
    rname=request.GET.get("rolename","")
    rnote=request.GET.get("note","")
    models.RoleInfo.objects.create(rolename=rname, note=rnote)
    return HttpResponse(json.dumps('suc'), content_type="application/json")
def rolemod(request,ectype,rid):
    rname=request.GET.get("rolename","")
    rnote=request.GET.get("note","")
    if ectype == "moddetail" : #进入角色查看页面
        obj = models.RoleInfo.objects.filter(id=rid).values("id","rolename","note").first()
        return render(request,"role-mod.html",{"obj":obj})
    elif ectype == "mod": #修改角色
        models.RoleInfo.objects.filter(id=rid).update(rolename=rname, note=rnote)
    return HttpResponse(json.dumps('suc'), content_type="application/json")
# @transaction.atomic
def roleset(request,rid,ids):
    ids=ids[0:len(ids)-1]
    rids = re.split(',', ids)
    models.RolemenuInfo.objects.filter(role_id=rid).delete()
    for i in rids:
        models.RolemenuInfo.objects.create(role_id=rid,menu_id=i)
    return HttpResponse(json.dumps('suc'), content_type="application/json")

# ----------------message--------------------
def sendmsg(request):
    userid = request.POST.get('userid')
    msg = request.POST.get('msg')
    models.MessgeInfo.objects.create(user=userid,message= msg,state=0)
    return HttpResponse(json.dumps('suc'), content_type="application/json")
def msglist(request):
    return render(request, "msg.html")
def loadmsg(request):
    userid = request.session.get("user_id")
    lis=list(models.MessgeInfo.objects.filter(user=userid,state=0).values("message","state"))

    reponse_data = {'code': 0, 'msg': '', 'count': len(lis), "data": lis}
    return HttpResponse(json.dumps(reponse_data), content_type="application/json")