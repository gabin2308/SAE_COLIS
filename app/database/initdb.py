
import sqlite3,os

from pathlib import Path

from flask import current_app,g

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(__file__)

schema_path = os.path.join(BASE_DIR, "schema.sql")

def get_db():

    if "db" not in g:

        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db



def close_db(e=None):

    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    from app import app
    with app.app_context():
        db_path = app.config["DATABASE"]
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        db = get_db()

        # 1. Création initiale si la base n'existe pas
        if not os.path.exists(db_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.commit()
        
        # 2. Ajout sécurisé de la colonne si elle est absente (Migration)
        try:
            db.execute("SELECT password_must_change FROM utilisateur LIMIT 1")
        except sqlite3.OperationalError:
            # La colonne n'existe pas, on l'ajoute
            db.execute("ALTER TABLE utilisateur ADD COLUMN password_must_change INTEGER NOT NULL DEFAULT 0")
            db.commit()

        app.teardown_appcontext(close_db)