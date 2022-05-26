"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import json
import os.path
from pathlib import Path
import pymysql
import allauth

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


secret_file = os.path.join(BASE_DIR, "./config/secrets.json")
secrets = None
with open(secret_file) as f:
    secrets = json.loads(f.read())

# Keep secret keys in secrets.json
def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = secrets['SECRET_KEY']
IAMPORT_KEY = secrets['IAMPORT_REST_API']
IAMPORT_SECRET = secrets['IAMPORT_SECRET']

SOCIAL_OUTH_CONFIG = {
    'KAKAO_REST_API_KEY': secrets['KAKAO_REST_API_KEY'],
    "KAKAO_REDIRECT_URI": secrets['KAKAO_REDIRECT_URI'],
    "KAKAO_SECRET_KEY": secrets['KAKAO_SECRET_KEY'],
    "KAKAO_ADMIN_KEY": secrets['KAKAO_ADMIN_KEY'],
    "NAVER_CLIENT_ID": secrets['NAVER_CLIENT_ID'],
    "NAVER_SECRET_KEY": secrets['NAVER_SECRET_KEY'],
    "NAVER_REDIRECT_URI" : secrets['NAVER_REDIRECT_URI']
}

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    #django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    #myApps
    'chat',
    'config',
    'users',
    'cafe',
    'comments',
    'order',
    'cart',
    #django-rest-auth

    #django-allauth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'django.contrib.sites',

    # #provider
    # 'allauth.socialaccount.providers.naver',

]



# provider 설정



#rest framework
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES' : (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES' : [
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#     ],
# }

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
CART_ID = 'cart_in_session'
LOGIN_REDIRECT_URL = '/'





# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_AUTHENTICATED_LOGOUT_REDIRECTS = True
# ACCOUNT_LOGOUT_REDIRECT_URL = "/"


AUTH_USER_MODEL = 'users.CustomUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ChatTime(AWS)',
        'USER': 'admin',
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': get_secret('DATABASE_HOST'),
        'PORT': get_secret('DATABASE_PORT'),
        'OPTIONS': {
            'init_command': 'SET sql_mode = "STRICT_TRANS_TABLES"'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



