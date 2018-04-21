# _*_coding:utf-8_*_
# _*_coding:utf-8_*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message=u'请登录'
mail = Mail()

db = SQLAlchemy()

def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config[config_type])
    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    Bootstrap(app)

    from auth import auth
    app.register_blueprint(auth)

    return app