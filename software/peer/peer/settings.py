"""
Django settings for peer project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '04ky(@*!6#my)+v9%++x7!lvl1h$f4@!ut%vdv$qq0v63+ou=-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['jeremych.zapto.org', 'sleepify.zapto.org', 'localhost', '127.0.0.1', '192.168.1.100', 'peer1', 'peer2', 'raspberrypi', '86.177.166.34']

# Application definition

INSTALLED_APPS = [
    'client',
    'alpr',
    'personal',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',

    # django_crons
    'django_cron',

    # bootstrap
    'bootstrap3',

    # django tables 2
    'django_tables2',

    # django facebook api
    #'django_facebook',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'peer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # live data
                'personal.context_processors.live_data',
                # default
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # django tables 2
                'django.template.context_processors.request',
                # django facebook
                #'django_facebook.context_processors.facebook',
            ],
        },
    },
]

WSGI_APPLICATION = 'peer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

#
# logging
#

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'encoding': 'utf-8'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/static/log.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', ],
            'level': 'INFO',
        },
    },
}

# AUTHENTICATION_BACKENDS = (
#     'django_facebook.auth_backends.FacebookBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
# List of directories where "./manage.py collectstatic" will look for files, which it puts all together into STATIC_ROOT. Each app that you have can have it's own "static" files directory.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # This is the "static" files directory where say most of the CSS/JS/IMG files are stored for the project.
)

# Physical system path where the static files are stored. Files that are being uploaded by the user.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that your MEDIA files will be accessible through the browser.
MEDIA_URL = '/media/'

BOOTSTRAP3 = {
    'include_jquery': True,
}

GEOIP_PATH = os.path.join(STATICFILES_DIRS[0], 'geolite2')

################# others

CRON_CLASSES = [
    # bootstrapping
    'client.cron.register.Register',
    'client.cron.keep_alive.Keep_Alive',
    'client.cron.keep_alive.Keep_Alive_Peer',
    'client.cron.deregister.Deregister',
    # peers
    'client.cron.get_peer_list.Get_Peer_List',
    'client.cron.share_plates.Share_Plates',
    'client.cron.modify_trust.Modify_Trust',
    'client.cron.violations.Detect_Violations',
    # alpr
    'alpr.cron.import_videos.Import_Videos',
    'alpr.cron.process_videos.Process_Videos',
]

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
######################## EE4 FYP SETTINGS HERE #########################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

MY_NAME = "Jeremy Chan"

SHORT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 1

BOOTSTRAP_BASE_URL = 'http://bootstrap:34568/' # must include http or No connection adapters were found for ...

PEER_HOSTNAME = '86.177.166.34' # peer IP
PEER_PORT = 34571 # peer port

TRUST_THRESHOLD = 10 # what trust needed before sending

NO_PLATES_BATCH_BEFORE_SEND = 1 # howm
MIN_TRUST_FOR_SHARE_PLATES = 0 #TODO: test with 40
ADD_TRUST_MATCHING_PLATE = 10
TRUST_DECAY = 0.99

SPEEDING_LIMIT_PERCENT = 10
RESIDENTIAL_SPEED_LIMIT = 30

ALPR_FPS = 5
ALPR_VIDEO_PATH = '/home/pi/test_videos/walking/'
ALPR_IMAGES_PATH = '/home/pi/test_videos/walking'
ALPR_URL = '/alpr/'

# api keys + other keys
GOOGLE_MAPS_API_KEY = 'AIzaSyAa6ZK81sMBK2dVrGcOVaWhKUVyfvyUft8'
FERNET_KEY = b'a0SThzUK3EFVlxbZ5_3ru1ou2vWShkGR6Ca_RV7kvWQ='

FACEBOOK_APP_ID = '1786476698345753'
FACEBOOK_APP_SECRET = 'f79b9408f02e05fa2ec9b14ab3e0895b'

TWITTER_CONSUMER_KEY = 'aUe3p3vkiih5tVoOr9NwQfklw'
TWITTER_CONSUMER_SECRET = 'hlsGz9o8ZlUtUrRM5PVUlgWXCur1Fr54KUkJ4qRoZAEqIC4kYt'
TWITTER_ACCESS_TOKEN_KEY = '398428540-pU1SxHhVZlU09WSt5Jo7AofhNBkXZWI47YyMSHpu'
TWITTER_ACCESS_TOKEN_SECRET = 'J3RqksPucuON7uQDafXScxUinxknHwTGPDsUH8JLVBuH2'

