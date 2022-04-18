from pathlib import Path

class Config(object):
    DEBUG = False
    SECRET_KEY = 'qpzRL7LXpk7FU8_9HjtcAA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('database.sqlite'))


class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    ENV = 'testing'
    DEBUG = True
