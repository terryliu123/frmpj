from django.shortcuts import render,HttpResponse,redirect
import re,json
from datetime import datetime
from django.db.models import Count,Q
from aip import AipOcr





def test(request):
    return render(request, "test.html")
def ocrai(request):
    # 定义常量
    APP_ID = '11963255'
    API_KEY = 'sk530p40dC9zeAPEfv3QsRKU'
    SECRET_KEY = 'kjK7BniOOtZgAzDUebixZSlK1HlVcZZo'
    # 初始化AipFace对象
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 读取图片
    url = request.POST.get('url')
    print(url)
    filePath ='C:/pythondev/timg.jpg'
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

def piccheck():
    APP_ID = '14131784'
    API_KEY = 'nAfbeuX0qj6ksjHIZGGzecCn'
    SECRET_KEY = 'XMXqW4GPjQ8aVoZvQUXPo2IXFN5aG6Qn '
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    IMAGE_TYPE = 'BASE64'

    f1 = open('C:/pythondev/1.jpg', 'rb')
    f2 = open('C:/pythondev/2.jpg', 'rb')
    # 参数image：图像base64编码 分别base64编码后的2张图片数据
    img1 = base64.b64encode(f1.read())
    img2 = base64.b64encode(f2.read())
    image_1 = str(img1, 'utf-8')
    image_2 = str(img2, 'utf-8')

    ptr = client.match([
        {
            'image': image_1,
            'image_type': 'BASE64',
        },
        {
            'image': image_2,
            'image_type': 'BASE64',
        }
    ])
    ptr = ptr['result']
    print(ptr)
    if ptr['score'] <= 50:
        print('这俩人不像：哈哈哈', ptr['score'])
    else:
        print('piupiupiu：孪生兄弟啊', ptr['score'])
    return HttpResponse(json.dumps(ptr), content_type="application/json")


