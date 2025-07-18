import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',"this-is-test-secret-key")


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True
    
  