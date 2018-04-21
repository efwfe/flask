# _*_coding:utf-8_*_

# _*_coding:utf-8_*_

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:zhang@localhost:3306/flask"
    FLASKY_POST_PER_PAGE = 25
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    SECRET_KEY = 'ADADADADS-'
    MAIL_SERVER ="smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USER_TLS= True
    MAIL_USE_SSL = True
    FLASK_MAIL_SUBJECT_PREFIX = '[GREENLAND]'
    MAIL_USERNAME ='471404259@qq.com'
    MAIL_PASSWORD = 'ftjqeqjsfcwacbdh'
    FLASK_MAIL_SENDER = '471404259@qq.com'

class ProConfig(Config):
    DEBUG=False
    pass

config = {
    'develop':DevConfig,
    'production':ProConfig,
}