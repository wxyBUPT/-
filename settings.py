#coding=utf-8
DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'bdms_web',                      # Or path to database file if using sqlite3.
#        'USER': 'bdms',                      # Not used with sqlite3.
#        'PASSWORD': 'bdms',                  # Not used with sqlite3.
#        'HOST': '172.18.2.40',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
#    }
}

INSTALLED_APPS = (
    'ide',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    )

SECRET_KEY = '143333'

TIME_ZONE='Asia/Shanghai'
TEMPLATE_DIRS = (
    u"C:\\Users\\BFD_504\\Desktop\\调度传参\\template",
)