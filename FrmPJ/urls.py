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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('welcome/', views.welcome),
    path('member-list/', views.memberlist),
    path('member-add/', views.memberadd),
    path('member-del/', views.memberdel),
    path('member-edit/', views.memberedit),
    path('member-pwd/', views.memberpwd),
    path('orgtree/', views.orgtree),
    #-----------------------------------
    path('login/', views.login),
    # 人员信息管理
    path('p-page/', views.personpage),
    path('p-list/', views.personlist),
    path('p-detail/<str:ectype>/<str:pid>/', views.persondetail),
    path('person/<str:ectype>/<str:pid>/<str:state>/', views.person),
    path('checkuser/<str:username>/', views.checkuser),
    path('modpwd/<str:ectype>/<str:pid>/', views.modpwd),

 ]
