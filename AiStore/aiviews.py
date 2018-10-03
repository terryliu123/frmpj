
from django.shortcuts import render,HttpResponse,redirect
from SysMGR import models
import re,json,os,face_recognition,pytesseract,time,cv2
from datetime import datetime
from django.db.models import Count,Q
from AiStore import sl_face
from PIL import Image
from SysMGR import views
# 人脸识别操作页面
def upload(request):
    obj = list(models.UserInfo.objects.filter().values('id', 'username', 'person__pname'))
    return render(request, "upload.html",{'userlist':obj})
# ocr页面
def ocrpage(request):
    return render(request, "upload-ocr.html")
# 人脸页面
def facepage(request):
    return render(request, "face-page.html")
# 人脸登陆
def facelogin(request):
    imgfile = request.FILES.get('file')
    filename = str(time.time())+".jpg"
    img_path = os.path.join('static/images/',filename)    #存储的路径
    print(img_path)
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
    f.close()
    image = face_recognition.load_image_file(img_path)
    face_landmarks_list = face_recognition.face_landmarks(image)
    ret={}
    if len(face_landmarks_list) <1 :
        ret = {'code': False, 'data': img_path}  # 'data': img_path 数据为图片的路径，
        os.remove(img_path)
        return HttpResponse(json.dumps(ret))  # 将数据的路径发送到前端
    # 读取图片并识别人脸
    name = sl_face.loadface(img_path)
    ret = {'code': False, 'data': img_path, 'name': name}  # 'data': img_path 数据为图片的路径，
    os.remove(img_path)
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
@views.user_session_filter
def findex(request):
    if request.session["user_id"] == "":
        return render(request, "login.html", {'error_msg': '用户名密码错误！'})
    menulist = views.rolemenu(request.session["role_id"])
    msgcount = models.MessgeInfo.objects.filter(user= request.session["user_id"]).aggregate(c=Count('id'))
    return render(request, "index.html", {'menulist': menulist, 'username':  request.session["username"], "msgcount": msgcount['c']})
# 上传文字性图片
def upload_ocr(request):
    filename= str(time.time())+".jpg"
    imgfile = request.FILES.get('file')
    img_path = os.path.join('static/images/',filename)    #存储的路径
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
    f.close()
    image = Image.open(img_path)
    cont = pytesseract.image_to_string(image, lang='chi_sim')
    print(cont)
    ret = {'code': True, 'data': img_path,'content':str(cont)}  # 'data': img_path 数据为图片的路径，
    os.remove(img_path)
    return HttpResponse(json.dumps(ret))    #将数据的路径发送到前端
# 上传图片，生成识别特征码
def upload_file(request):
    filename= request.POST.get("filename")
    imgfile = request.FILES.get('file')
    img_path = os.path.join('static/images/face/',filename+".jpg")    #存储的路径
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
    f.close()
    image = face_recognition.load_image_file(img_path)
    face_landmarks_list = face_recognition.face_landmarks(image)
    ret={}
    if len(face_landmarks_list) <1 :
        ret = {'code': False, 'data': img_path}  # 'data': img_path 数据为图片的路径，
        os.remove(img_path)
    else:
        sl_face.saveface()  # 重新生成特征识别码库
        ret = {'code': True, 'data': img_path}  # 'data': img_path 数据为图片的路径，
    return HttpResponse(json.dumps(ret))    #将数据的路径发送到前端
# -------------------------------------------------------------------------
def vface(request):
    return render(request, "face-video.html")
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
        name = sl_face.loadface(filename)
        cv2.putText(img, name[i], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # 显示识别结果
    cv2.imwrite(filename, img)
def videof(request):
    imgfile = request.FILES.get('file')
    filename = str(time.time())+".jpg"
    img_path = os.path.join('static/images/videoface',filename)    #存储的路径
    print(img_path)
    with open(img_path,'wb') as f:      #图片上传
        for item in imgfile.chunks():
            f.write(item)
        f.close()
    image = face_recognition.load_image_file(img_path)
    face_landmarks_list = face_recognition.face_landmarks(image)
    ret={}
    # 监测是否有人脸
    if len(face_landmarks_list) <1 :
        ret = {'code': False, 'data': img_path}  # 'data': img_path 数据为图片的路径，
        os.remove(img_path)
    else:
        painface(img_path)
        ret = {'code': True, 'data': img_path}  # 'data': img_path 数据为图片的路径，
    return HttpResponse(json.dumps(ret))    #将数据的路径发送到前端
def delface(request):
    # os.path.join('static/images/videoface/', filename)
    filename=request.GET.get('filename')
    print(filename)
    os.remove(filename)
    print('ok')
    return HttpResponse(json.dumps('suc'))  # 将数据的路径发送到前端
