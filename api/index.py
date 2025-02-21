import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Get the project root directory
project_root = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(project_root / '.env.development.local')

# Add the project root directory to Python path
sys.path.append(str(project_root))

# Print environment variables for debugging
print("Loading environment variables...")
print("POSTGRES_URL:", os.environ.get('POSTGRES_URL'))

from flask import Flask
from extensions import init_extensions, db, migrate
from app.models import Admin, Article, Category

def create_app():
    app = Flask(__name__, 
        template_folder='../app/templates',
        static_folder='../app/static',
        instance_relative_config=True
    )

    # 기본 설정
    app.config.from_object('config.Config')
    
    # 데이터베이스 URL이 없으면 에러
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise RuntimeError(
            'POSTGRES_URL environment variable is not set. '
            'Please check your .env.development.local file.'
        )
    
    # 데이터베이스 초기화
    init_extensions(app)
    
    # Print configuration for debugging
    print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Import and register blueprints
    from app.main.routes import bp as main_bp
    from app.auth.routes import bp as auth_bp
    from app.admin.routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

def setup_database(app):
    """데이터베이스 초기 설정"""
    with app.app_context():
        # 데이터베이스 테이블 생성
        db.create_all()
        
        # 카테고리 초기화
        categories = [
            {'name': '정치', 'slug': 'politics'},
            {'name': '경제', 'slug': 'economy'},
            {'name': '사회', 'slug': 'society'},
            {'name': '문화', 'slug': 'culture'},
            {'name': '국제', 'slug': 'international'},
            {'name': 'IT', 'slug': 'it'},
            {'name': '스포츠', 'slug': 'sports'}
        ]
        
        for cat_data in categories:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                category = Category(name=cat_data['name'], slug=cat_data['slug'])
                db.session.add(category)
        
        # 관리자 계정 생성
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@example.com')
            admin.set_password('password')
            db.session.add(admin)
        
        try:
            db.session.commit()
            print("Database initialized successfully")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")
            raise

app = create_app()

# For Vercel
application = app

if __name__ == '__main__':
    try:
        setup_database(app)
    except Exception as e:
        print(f"Failed to setup database: {e}")
    
    app.run(debug=True) 