import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = 'uey!i4x26n!$d-73cs%blri)09#xfud_e361ne2h(#s2uj7)l!'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'df_cart',
    'df_goods',
    'df_user',
    'df_order',

    'tinymce',  # Using a rich text editor requires installation in the settings file
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

ROOT_URLCONF = 'tiaozao_shop.urls'

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
                'django.template.context_processors.media',  # Register media_url upload path in templates
            ],
        },
    },
]

WSGI_APPLICATION = 'tiaozao_shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tiaozao',   # Database name
        'USER': 'root',      # Username
        'PASSWORD': '123456',  # Password
        'HOST': '127.0.0.1',  # Localhost
        'PORT': '3306'        # Port number
    }
}

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

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'zh-hans'  # Change admin panel to Chinese

TIME_ZONE = 'Asia/Shanghai'  # Set timezone to Shanghai

USE_TZ = False  # The database uses international time

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
# Set the path for uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Specify root directory

# Configuration for using the rich text editor
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

# Email sending settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False  # Whether to use TLS security protocol (provides confidentiality and data integrity between applications)
EMAIL_USE_SSL = True  # Whether to use SSL encryption, required by QQ enterprise email
EMAIL_HOST = 'smtp.163.com'  # SMTP server of the email sender (163 mail used here)
EMAIL_PORT = 465  # SMTP server port of the sending email
EMAIL_HOST_USER = 'woaisilaowu@163.com'  # Email address for sending emails
EMAIL_HOST_PASSWORD = 'PZDOHBIYHAJSCVPS'   # Email password (authorization code used here)
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
