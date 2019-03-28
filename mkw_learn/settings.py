"""
Django settings for mkw_learn project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,os.path.join(BASE_DIR,'apps')) #将apps放到环境变量中
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps')) #将extra_apps放到环境变量中


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4+2&bdpgf*7z$^oc1$s4pu)h2n0%l7#8(ad21v$mjo)@c*w_vs'

# SECURITY WARNING: don't run with debug turned on in production!


#测试环境下
DEBUG = True

ALLOWED_HOSTS = []   #允许访问的端口

#生产环境
# DEBUG = False
# ALLOWED_HOSTS = ['*']   #ALLOWED_HOSTS = ['*'] :所有端口都可访问




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'organization',
    'operation',
    'course',
    'xadmin',
    'crispy_forms',
    'captcha',#验证码
    'DjangoUeditor',#富文本编辑
]

#自定义用户 重载AUTH_USER_MODEL
AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mkw_learn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #添加图片处理器，为了在课程列表中前面加上MEDIA_URL
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mkw_learn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

#配置mysql数据库
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'mkw_learn', #数据库名字
    'USER': 'root', #账号
    'PASSWORD': '1234', #密码
    'HOST': '', #IP
    'PORT': '3306', #端口
}
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#DEBUG=True,测试环境下,django后台自动配置静态文件
STATIC_URL = '/static/'

#静态文件绝对路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)


#DEBUG=False,生产环境下,django不会配置静态文件.
# STATIC_URL = '/static/'
#
# #配置静态文件路径
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')




#配置邮箱
EMAIL_HOST = "smtp.qq.com"  # SMTP服务器主机
EMAIL_PORT = 25             # 端口
EMAIL_HOST_USER = "2962883712@qq.com"       # 邮箱地址
EMAIL_HOST_PASSWORD = "pjlmzdoargbtddhb"    # 使用qq邮箱时,这里是授权码
EMAIL_USE_TLS= False
EMAIL_FROM = "2962883712@qq.com"            # 邮箱地址



# 设置上传文件的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')   #指定上传文件的绝对路径















