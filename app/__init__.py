from flask import Flask
from flask_cors import CORS
from config import Config
from app.database.initdb import init_db
from app.controller import register_all
from app.extensions import bcrypt, limiter

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
bcrypt.init_app(app)
limiter.init_app(app)

init_db()

register_all(app)  # découvre et enregistre tous les controllers automatiquement
print(app.url_map)