from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_pagedown import PageDown


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 账户认证相关，包括了注册
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    # url_prefx指定该蓝图的url的前缀，简化该蓝图的路由函数的参数
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
