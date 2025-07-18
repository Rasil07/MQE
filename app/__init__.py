from flask import Flask
from app.config import  DevelopmentConfig, ProductionConfig, TestingConfig


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def create_app(config_class_name='development'):
    print(f"Config: {config_class_name}")
    app = Flask(__name__, template_folder='templates',static_folder='static')
    app.config.from_object(config_dict[config_class_name])
    print(f"Config: {config_dict[config_class_name]}")
    from app.routes import main
    app.register_blueprint(main)

    return app