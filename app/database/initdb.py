
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
        
        db_exists = os.path.exists(db_path) and os.path.getsize(db_path) > 0

        db = get_db()

        if not db_exists:
            with open(schema_path, "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.commit()

        app.teardown_appcontext(close_db)