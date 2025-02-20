from app import create_app

app = create_app()

# Vercel requires the app to be named 'app'
application = app 