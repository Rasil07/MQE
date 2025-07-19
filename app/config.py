import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',"this-is-test-secret-key")
    UPLOAD_FOLDER = "uploads"
    DATABASE_PATH = "store/database.db"
    DATABASE_SCHEMA = "app/schema/schema.sql"
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True
    
  