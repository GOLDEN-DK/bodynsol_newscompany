from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import event, select
from sqlalchemy.exc import OperationalError
import time

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_extensions(app):
    # 데이터베이스 초기화
    db.init_app(app)
    
    # 로그인 매니저 초기화
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Flask-Migrate 초기화
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요한 페이지입니다.'
    login_manager.login_message_category = 'warning'
    
    # 애플리케이션 컨텍스트 내에서 이벤트 리스너 설정
    with app.app_context():
        engine = db.get_engine()
        
        @event.listens_for(engine, 'connect')
        def connect(dbapi_connection, connection_record):
            print('Connection established')

        @event.listens_for(engine, 'engine_connect')
        def ping_connection(connection, branch):
            if branch:
                return

            try:
                connection.scalar(select(1))
            except Exception:
                connection.connection.close()
                connection.connection = None
                raise 