from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Flask-Migrate 초기화
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요한 페이지입니다.'
    login_manager.login_message_category = 'warning' 