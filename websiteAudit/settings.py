"""
Django settings for websiteAudit project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# This docstring provides information about the file's purpose and its origin. It specifies that the file contains
# settings for the 'websiteAudit' Django project and mentions the Django version used to generate it. The links
# provide more details about Django settings and their documentation.

from pathlib import Path
import os

# This import statement brings in the Path class from the pathlib module, which is used for filesystem path
# manipulations.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR is a Path object representing the base directory of the Django project. It is calculated relative to the
# location of this settings file.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-...'
# SECRET_KEY is a critical setting that's used for cryptographic signing. It should be kept secret, especially in
# production.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG is a boolean that turns on/off debug mode. It should be False in production for security reasons.

ALLOWED_HOSTS = []
# ALLOWED_HOSTS is a list of strings representing the host/domain names that this Django site can serve.


# Application definition

# INSTALLED_APPS is a list of all Django applications that are activated in this Django instance.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'report_generator',
    'website_analyzer',
    'api',
    'corsheaders',
]

# MIDDLEWARE is a list of middleware classes that are run during request/response processing.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Add the origin of your HTML page
    # Add more origins if needed
]

# ROOT_URLCONF is a string representing the dotted path to the URL configuration module for the project.
ROOT_URLCONF = 'websiteAudit.urls'

# TEMPLATES is a list of template configurations. Django uses this to find and render templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

# WSGI_APPLICATION is the dotted path to the WSGI application object that Django's built-in servers use.
WSGI_APPLICATION = 'websiteAudit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES is a dictionary containing the settings for all databases to be used with this Django project.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS is a list of validators that are used to check the strength of user passwords.
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# These settings are for internationalization and timezone settings.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL is the URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD is a string defining the type of primary key to use for models that don’t specify a field with
# 'primary_key=True'.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
# print(MEDIA_ROOT)
MEDIA_URL = '/media/'
