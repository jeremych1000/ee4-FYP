"""
Django settings for bootstrapping project.

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
SECRET_KEY = '_i_+e0(7-3g!&$4l_0mck(aw+sn1piq5)9^k_izm8qba4vz3w-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['jeremych.zapto.org', 'sleepify.zapto.org', 'localhost', '127.0.0.1', '192.168.1.100', 'bootstrap', 'raspberrypi']

# Application definition

INSTALLED_APPS = [
    'bootstrap',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',

    # django_crons
    'django_cron',

    
    # bootstrap
    'bootstrap3',
    
    'django_extensions',
    
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

ROOT_URLCONF = 'bootstrapping.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'bootstrapping.wsgi.application'

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


CRON_CLASSES = [
    'bootstrap.cron.prune_alive.Prune_Alive',
    'bootstrap.cron.minutes_connected.Minutes_Connected',
    'bootstrap.cron.peer_broadcast.Update_Tokens',
]
DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 1

GOOGLE_MAPS_API_KEY = 'AIzaSyAa6ZK81sMBK2dVrGcOVaWhKUVyfvyUft8'
FERNET_KEY = b'a0SThzUK3EFVlxbZ5_3ru1ou2vWShkGR6Ca_RV7kvWQ='