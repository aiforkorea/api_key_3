# apps/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

#    app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates"))
#    app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    # 블루프린트 등록
    from .auth import auth as auth_bp
    from .main import main as main_bp
    from .iris import iris as iris_bp
#    from .admin import admin as admin_bp
#    from .mypage import mypage as mypage_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(iris_bp, url_prefix='/iris')
#    app.register_blueprint(admin_bp, url_prefix='/admin')
#    app.register_blueprint(mypage_bp, url_prefix='/mypage')

    # 관리자 계정 자동생성
    with app.app_context():
        from .auth.models import User, create_admin
        db.create_all()
        create_admin()

    return app

