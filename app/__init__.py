from flask import Flask
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.Sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()
mail =Mail()
moment = Moment()
db = SQLAlchemy()#隐含了许多步骤，engine等具体见官网示例

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view=''#待完善

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config.__init__(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app

















