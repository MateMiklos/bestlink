from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os

bp = Blueprint("main", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "instance", "bestlink.db")

@bp.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT books.id, books.title, books.author, books.price, categories.name
        FROM books
        LEFT JOIN categories ON books.category_id = categories.id
        ORDER BY books.title
    """)
    books = c.fetchall()
    conn.close()
    return render_template("index.html", books=books)

@bp.route("/add", methods=["GET", "POST"])
def add_book():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        category = request.form["category"]

        c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
        c.execute("SELECT id FROM categories WHERE name=?", (category,))
        category_id = c.fetchone()[0]

        c.execute(
            "INSERT INTO books (title, author, price, category_id) VALUES (?, ?, ?, ?)",
            (title, author, price, category_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("main.index"))
    else:
        c.execute("SELECT name FROM categories ORDER BY name")
        categories = [r[0] for r in c.fetchall()]
        conn.close()
        return render_template("add_book.html", categories=categories)

@bp.route("/delete/<int:book_id>")
def delete_book(book_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("main.index"))
