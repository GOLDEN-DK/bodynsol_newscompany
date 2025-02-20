# Empty file to make the directory a Python package 

def create_app():
    # ...
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    # ... 