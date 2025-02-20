import os
import sys
from dotenv import load_dotenv
from pathlib import Path

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
from api.extensions import init_extensions, db
from app.models import Admin, Article

def create_app():
    app = Flask(__name__, 
        template_folder='../app/templates',
        static_folder='../app/static',
        instance_relative_config=True
    )

    # Basic config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    
    # Database URL configuration
    postgres_url = os.environ.get('POSTGRES_URL')
    if not postgres_url:
        raise RuntimeError(
            'POSTGRES_URL environment variable is not set. '
            'Please run "vercel env pull .env.development.local" to get your environment variables.'
        )
    
    # Convert postgres:// to postgresql:// if necessary
    if postgres_url.startswith('postgres://'):
        postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Vercel specific configuration
    app.config['INSTANCE_PATH'] = '/tmp'  # Use /tmp directory instead
    app.instance_path = '/tmp'  # Override instance path

    # 환경 설정
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

    # Initialize extensions
    init_extensions(app)
    
    # Print configuration for debugging
    print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Import routes
    from app.main.routes import bp as main_bp
    from app.auth.routes import bp as auth_bp
    from app.admin.routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

app = create_app()

# For Vercel
application = app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@example.com')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 