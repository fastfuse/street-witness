
import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x3fp'
                                '\x16#Z\x0b\x81\xeb\x16')

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# export APP_SETTINGS="config.DevelopmentConfig"
# export DATABASE_URL="postgresql://witness:street@localhost/street_witness"