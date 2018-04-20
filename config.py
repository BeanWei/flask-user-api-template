import logging

APP_ENV = "testing"

class BaseConfig:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #是否开启跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "hello"
    '''
    根据需求添加相关配置
    '''


class TestingConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@localhost:3306/test"

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@localhost:3306/test"

config = {
    "testing": TestingConfig,
    "devolopment": DevelopmentConfig
}