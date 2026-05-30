from flask import Flask, session, jsonify, request
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import importlib
import os
from flask_cors import CORS
from config import Config
from app.database.initdb import init_db
from app.controller import register_all
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__, static_url_path="/static")
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.secret_key = os.getenv("SECRET_KEY")
app.config.from_object(Config)

FRONTEND_URL = os.getenv("FRONTEND_URL")
CORS(app,origins=["http://localhost:5173"],
     supports_credentials=True)

bcrypt = Bcrypt()

bcrypt.init_app(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "200 per hour", "60 per minute"],
    default_limits_exempt_when=lambda: request.path == "/api/auth/me"
)

init_db()

register_all(app)  
print(app.url_map)