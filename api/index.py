# api/index.py

from asgiref.wsgi import WsgiToAsgi
from app import create_app

flask_app = create_app()
asgi_app = WsgiToAsgi(flask_app)

# Vercel looks for a variable called `handler`
handler = asgi_app
