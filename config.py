# ----------------------------------------------------------------------------------------------------------------------
# Create configuration
class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 4}
    # SERVER_NAME = '127.0.0.1:10001'
