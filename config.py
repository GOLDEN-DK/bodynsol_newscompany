import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    # Use PostgreSQL URL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # SSL 설정 추가
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'sslmode': 'require',
            'connect_timeout': 10
        },
        'pool_pre_ping': True,  # 연결 상태 확인
        'pool_recycle': 300,    # 5분마다 연결 재생성
        'pool_timeout': 30      # 연결 타임아웃 30초
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False 