import os

ALLOWED_HOSTS = ['*']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***********************'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myapp',
        'USER': 'user_django',
        'PASSWORD': '*****************',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = True
