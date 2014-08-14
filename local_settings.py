__author__ = 'roxnairani'

DATABASES = {
    'default':
         {'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'rad',}
}

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

TASTYPIE_FULL_DEBUG = True