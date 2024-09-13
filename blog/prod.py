from .settings import *

ALLOWED_HOSTS = ['dioulde.pythonanywhere.com',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dioulde$default',
        'USER': 'dioulde',
        'PASSWORD': 'kindy2403',
        'HOST' : 'dioulde.mysql.pythonanywhere-services.com',
        'PORT' : '3306',
    }
}