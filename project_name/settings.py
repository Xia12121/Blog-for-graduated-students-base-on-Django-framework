import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '203002616510086'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'app_name',
]

# 更改默认语言为中文
LANGUAGE_CODE = 'zh-hans'
 
 # 去掉默认Logo或换成自己Logo链接
SIMPLEUI_LOGO = 'https://pic3.zhimg.com/80/v2-beefbfc9debdca87a6691f633449639c_qhd.jpg'
 
'''SIMPLEUI_CONFIG = {
    'menus': [
        {
            'app': 'app_name',
            'models': [
                {
                    'name': 'User',
                    'icon': 'fa fa-user',
                },
                {
                    'name': 'Case',
                    'icon': 'fa fa-briefcase',
                },
                {
                    'name': 'Article',
                    'icon': 'fa fa-newspaper',
                },
                {
                    'name': 'Like',
                    'icon': 'fa fa-thumbs-up',
                },
                {
                    'name': 'Comment',
                    'icon': 'fa fa-comments',
                },
                {
                    'name': 'PrivateMessage',
                    'icon': 'fa fa-envelope',
                },
                {
                    'name': 'Feedback',
                    'icon': 'fa fa-comment',
                },
                {
                    'name': 'TeamIntroduction',
                    'icon': 'fa fa-info-circle',
                },
                {
                    'name': 'TeamMember',
                    'icon': 'fa fa-users',
                },
                {
                    'name': 'worker',
                    'icon': 'fa fa-user-tie',
                },
                {
                    'name': 'FeaturedArticle',
                    'icon': 'fa fa-star',
                },
                {
                    'name': 'Alumni',
                    'icon': 'fa fa-graduation-cap',
                },
                {
                    'name': 'Offer',
                    'icon': 'fa fa-handshake',
                },
                {
                    'name': 'Tag',
                    'icon': 'fa fa-tags',
                },
                {
                    'name': 'UserLoginRecord',
                    'icon': 'fa fa-sign-in-alt',
                },
            ],
        },
        {
            'name': '控制面板',
            'icon': 'fa fa-eye',
            'url': '/dashboard/',
        },
    ],
}'''
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_name.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'APP_DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'software.engineering.project.testing.cpolar.top','test.gps.cpolar.top']

WSGI_APPLICATION = 'project_name.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

CORS_ALLOW_METHODS = [
    'GET', 
    'OPTIONS', 
    'HEAD', 
    'POST', 
    'PUT', 
    'DELETE',
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:1234',
    'http://localhost:1234',
    'http://127.0.0.1:8123',
    'http://localhost:8123',
    'http://tryplay.cpolar.top',
    'https://tryplay.cpolar.top',
    'http://test.gps.cpolar.top',
    'https://test.gps.cpolar.top',
]


CORS_ALLOW_CREDENTIALS = True

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_COOKIE_AGE = 86400

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app_name', 'static'),
    os.path.join(BASE_DIR, 'app_name', 'static', 'avatars'),
    os.path.join(BASE_DIR, 'app_name', 'static', 'offers')
]
