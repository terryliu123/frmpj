"""
Django settings for FrmPJ project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import djcelery
from AiStore import sl_face


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pazm-!d(&x87)0-xxlrzbr--+yz1*2v^pt)^%g*0o@93sij&=#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djcelery',
    'SysMGR',
    'FrmPJ',
    'Store',
    'AiStore',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FrmPJ.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')] ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'SysMGR.globalset.global_setting',
            ],
        },
    },
]

WSGI_APPLICATION = 'FrmPJ.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {               # mysql
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'frmpj',
        'USER': 'frmpjserver%lugertech',
        'PASSWORD': 'Lugertech_123',
        'HOST': 'frmpjserver.mysqldb.chinacloudapi.cn',
        'PORT': '3306',
        # 'ATOMIC_REQUESTS':True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ('images', os.path.join(STATIC_ROOT, 'images').replace('\\', '/')),
    ('font', os.path.join(STATIC_ROOT, 'font').replace('\\', '/')),
    # ('upload', os.path.join(STATIC_ROOT, 'upload').replace('\\', '/')),
)

# session setting Database Engine
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）

SESSION_COOKIE_DOMAIN = None             # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False            # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True           # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1800             # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False       # 是否每次请求都保存Session，默认修改之后才保存（默认）
# 这个好。settings里设为true，超时时间按照最后一次客户端请求计算，如上按照最后一次请求之后10秒失效。


# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# djcelery.setup_loader()
# BROKER_URL = 'amqp://guest@localhost//'
# BROKER_POOL_LIMIT = 0
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 28800}

SITE_NAME = 'Luger PreSales Framework'
COPY_RIGHT = 'Copyright ©2017-2018 Lugertech All Rights Reserved'