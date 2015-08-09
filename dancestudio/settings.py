"""
Django settings for dancestudio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3!jvl^a_$ms^d-v!)$yd%48xv!=1vj_j)ao8zr2ua3d0wn&siu'

# SECURITY WARNING: don't run with debug turned on in production!
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/sway/dashboard'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Absolute path to the media directory

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'sway',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'push_notifications',
    'django_crontab',
)

CRONJOBS = [
    ('*/1 * * * *', 'sway.cron.followup_notification_job')
]

PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": 'AIzaSyAQDwBHbz-VyiTnizycexakz3OGvrcQoEQ',
         # Use it for iOS device push notification "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
}
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

ROOT_URLCONF = 'dancestudio.urls'

WSGI_APPLICATION = 'dancestudio.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
)

CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'withcredentials',
        #'x-csrftoken',
)


CORS_ALLOW_CREDENTIALS = True

'''CORS_ORIGIN_WHITELIST = (
        'http://localhost:8080',
        'http://192.168.0.1:8000',                
        'http://192.168.122.132:3000',
        'http://192.168.121.20:3000',
)
'''

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2', 
'NAME': 'ebdb',
'USER': 'sway',
'PASSWORD': 'dbV1n33t!',
'HOST': 'aa1o3ryiohkl06q.cjeyqo71dm0x.us-west-2.rds.amazonaws.com:5432',   # Or an IP Address that your DB is hosted on
'PORT': '5432',
}
}
# default port is 3306
# Parse database configuration from $DATABASE_URL
#DATABASES['default'] =  dj_database_url.config()

# Enable Connection Pooling (if desired)
#DATABASES['default']['ENGINE'] = 'django_postgrespool'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/' # You may find this is already defined as such.

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)

LOGIN_URL='/sway/members/login'
'''
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)
'''
