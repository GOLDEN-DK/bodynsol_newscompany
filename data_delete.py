import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
project_root = Path(__file__).parent

# Load environment variables from .env file
load_dotenv(project_root / '.env.development.local')

# Add the project root directory to Python path
sys.path.append(str(project_root))

# Import after setting up the path
from api.index import app
from extensions import db  # api. 제거
from app.models import Admin, Category

def init_db():
    with app.app_context():
        # 1. 모든 테이블 삭제
        db.drop_all()
        print("All tables dropped.")
        
        # 2. 테이블 새로 생성
        db.create_all()
        print("New tables created.")
        
        # 3. 카테고리 생성
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
            category = Category(name=cat_data['name'], slug=cat_data['slug'])
            db.session.add(category)
        print("Categories added.")
        
        # 4. 관리자 계정 생성
        admin = Admin(username='admin', email='admin@example.com')
        admin.set_password('password')
        db.session.add(admin)
        print("Admin account created.")
        
        # 5. 변경사항 저장
        db.session.commit()
        print("All changes committed.")
        
        # 6. 테이블 구조 확인
        print("\nVerifying database structure:")
        for table in db.metadata.tables.values():
            print(f"\nTable: {table.name}")
            for column in table.columns:
                print(f"  - {column.name}: {column.type}")

if __name__ == "__main__":
    init_db()