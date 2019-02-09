"""
Django settings for yunke project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'static'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+h0wc@j1+n&g(=&zey#_b^al6*k#3hz)9o*c^ax8)u*p4e5ol8'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG=False
if not DEBUG:
    TEMPLATES_LOADERS=(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    TEMPLATES_LOADERS=(
        'django.template.loaders.cached.Loader',(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    )

ALLOWED_HOSTS = ['*'] #允许访问的ip地址


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'course',
    'operation',
    'organization',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',

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

ROOT_URLCONF = 'yunke.urls'
#此处重载是为了使我们的UserProfile生效
AUTH_USER_MODEL = 'users.UserProfile'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'yunke.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mooc',
        'USER':"root",
        "PASSWORD":'',
        'HOST':'127.0.0.1',
        'PORT':3306,

    },

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





AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,'static')
# STATICFILES_DIRS = (BASE_DIR,'static')

STATIC_URL = '/static/'
STATIC_ROOT = 'static' ## 新增行
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, '/static/'), ##修改地方
]


#设置上传文件的路劲
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#邮箱发送验证
EMAIL_HOST = 'smtp.qq.com'   #SMTP服务器主机
EMAIL_POST = 20      #端口
EMAIL_HOST_USER = "1580542048@qq.com"  #邮箱地址
EMAIL_HOST_PASSWORD="reyboxjnlueqfjbg"
EMAIL_USE_TLS = True
EMAIL_FROM = '1580542048@qq.com'    #邮箱地址





