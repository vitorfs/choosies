from unipath import Path
import dj_database_url

PROJECT_DIR = Path(__file__).parent

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'wmp&4oitf(kc@)t!%zg$edi1)$g8$2!cxvr0ch&#pw$h-j@i11'

DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'game',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'choosies.urls'

WSGI_APPLICATION = 'choosies.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {
  'default': dj_database_url.config(
    default = 'sqlite:///' + PROJECT_DIR.parent.child('db.sqlite3'))
}

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_DIR.parent.child('static'),
)

TEMPLATE_DIRS = (
    PROJECT_DIR.parent.child('templates'),
)