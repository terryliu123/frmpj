from django.shortcuts import render,HttpResponse,redirect
from SysMGR import models,forms
import re,json
from datetime import datetime
from django.db.models import Count,Q



def storagelist(request):
    return render(request, "storage-list.html")
def storageadd(request):
    return render(request, "storage-add.html")
def baidumap(request):
    return render(request, "baidumap.html")
def report(request):
    return render(request, "report.html")