"""FrmPJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SysMGR import views
from Store import storeviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('main/', views.main),
    path('orgtree/', views.orgtree),
    path('orgload/', views.orgload),
    path('orgec/<str:ectype>/', views.orgec),  # 移动组织
    #-----------------------------------
    path('login/', views.login),
    path('findex/', views.findex),
    # 人员信息管理
    path('p-page/', views.personpage),
    path('p-list/', views.personlist),
    path('p-detail/<str:ectype>/<str:pid>/', views.persondetail),
    path('person/<str:ectype>/<str:pid>/<str:state>/', views.person),
    path('checkuser/<str:username>/', views.checkuser),
    path('modpwd/<str:ectype>/<str:pid>/', views.modpwd),
    # 权限管理---------------------------------------------
    path('rolel/', views.rolel),
    path('role-list/', views.rolelist),
    path('role-page/', views.rolepage),
    path('role-add/', views.roleadd),
    path('role-mod/<str:ectype>/<str:rid>/', views.rolemod),
    path('role-menu/<str:roleid>/',views.rolemenulist),
    path('role-set/<str:rid>/<str:ids>/', views.roleset),
    #仓储管理-------------------------
    path('storage-list/', storeviews.storagelist),
    path('storage-add/', storeviews.storageadd),
    path('baidu-map/', storeviews.baidumap),
    path('report/', storeviews.report),
    #    ----------Msg---------------
    path('msglist/', views.msglist),
    path('loadmsg/', views.loadmsg),
    path('sendmsg/', views.sendmsg),

 #    AI------------------------------
    path('face-page/', views.facepage),
    path('upload/', views.upload),
    path('upload_file/', views.upload_file),
    path('ocr-page/', views.ocrpage),
    path('upload_ocr/', views.upload_ocr),
    path('facelogin/', views.facelogin),
    path('test/', views.test),
 ]



