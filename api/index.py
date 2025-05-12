from app import create_app

# This is the actual Flask app
app = create_app()

# Vercel expects this to be named "handler"
def handler(request, response):
    return app(request.scope, request.receive, request.send)