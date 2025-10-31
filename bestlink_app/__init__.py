from flask import Flask
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "instance", "bestlink.db")

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Initialize database
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                price REAL,
                stock INTEGER DEFAULT 0,           -- NEW COLUMN
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)

        conn.commit()

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
