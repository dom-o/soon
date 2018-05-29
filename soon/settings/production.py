from soon.settings.common import *
import os
import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production!
if ('DEBUG' in os.environ):
    DEBUG = os.environ['DEBUG']
else:
    DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

DATABASES['default'] = dj_database_url.config(conn_max_age=500)#, ssl_require=True)