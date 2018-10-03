from django.conf import settings  #调用settings
# Create your views here.
def global_setting(request):   #把setting方法读取出来
    return {
    'SITE_NAME': settings.SITE_NAME,   #返回定义的信息
    'COPY_RIGHT': settings.COPY_RIGHT,
    }
