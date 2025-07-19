from flask import Flask
from app.config import  DevelopmentConfig, ProductionConfig, TestingConfig
import os

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

UPLOAD_FOLDER = 'uploads'
DATABASE_FOLDER = 'store'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)


def create_app(config_class_name='development'):
    print(f"Config: {config_class_name}")
    app = Flask(__name__, template_folder='templates',static_folder='static')
    app.config.from_object(config_dict[config_class_name])
    print(f"Config: {config_dict[config_class_name]}")

    # Initialize database
    from app.database import Database
    db = Database(app.config['DATABASE_PATH'])
    db.initialize_tables(app.config['DATABASE_SCHEMA'])

    # Register file routes
    from app.modules.file.registrar import FileRegister
    FileRegister(app,db)
    return app