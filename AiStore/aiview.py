from django.shortcuts import render,HttpResponse,redirect
import re,json
from datetime import datetime
from django.db.models import Count,Q
from aip import AipOcr

# 定义常量
APP_ID = '11963255'
API_KEY = 'sk530p40dC9zeAPEfv3QsRKU'
SECRET_KEY = 'kjK7BniOOtZgAzDUebixZSlK1HlVcZZo'



def test(request):
    return render(request, "test.html")
def ocrai(request):
    # 初始化AipFace对象
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 读取图片

    url = request.POST.get('url')
    print(url)
    filePath =url
    # filePath = "C:\pythondev\denggao.jpeg"
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(filePath), options)
    return HttpResponse(json.dumps(result), content_type="application/json")

