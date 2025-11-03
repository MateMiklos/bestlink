from flask import Blueprint, render_template, request, redirect, url_for, flash
from bestlink_app.database import get_connection

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET"])
def index():
    """Homepage — show product list."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT 
            p.id,
            p.title,
            p.author,
            pt.name AS product_type,
            c2.name AS category,
            pub.name AS publisher,
            s.name AS supplier,
            p.price_in_huf,
            st.local_stock,
            st.gardners_stock
        FROM products p
        LEFT JOIN product_type pt ON p.product_type = pt.id
        LEFT JOIN categories c2 ON p.category = c2.id
        LEFT JOIN publishers pub ON p.publisher = pub.id
        LEFT JOIN suppliers s ON p.supplier = s.id
        LEFT JOIN stock st ON p.id = st.product_id
        ORDER BY p.title
    """)

    products = c.fetchall()
    conn.close()

    return render_template("index.html", products=products)


@bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    conn = get_connection()
    c = conn.cursor()

    if request.method == "POST":
        data = (
            request.form["isbn"],
            request.form["product_type"],
            request.form["title"],
            request.form["author"],
            request.form["category"],
            request.form["publisher"],
            request.form["supplier"],
            request.form["publication_date"],
            request.form["currency"],
            request.form["original_price"],
            request.form["sale_price"],
            request.form["price_in_huf"]
        )

        c.execute("""
            INSERT INTO products (
                isbn, product_type, title, author, category, publisher,
                supplier, publication_date, currency, original_price,
                sale_price, price_in_huf
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        product_id = c.lastrowid
        c.execute("INSERT INTO stock (product_id) VALUES (?)", (product_id,))
        conn.commit()
        conn.close()

        flash("✅ Product added successfully!", "success")
        return redirect(url_for("main.index"))

    # Dropdowns
    c.execute("SELECT id, name FROM product_type")
    product_types = c.fetchall()
    c.execute("SELECT id, name FROM categories")
    categories = c.fetchall()
    c.execute("SELECT id, name FROM publishers")
    publishers = c.fetchall()
    c.execute("SELECT id, name FROM suppliers")
    suppliers = c.fetchall()
    c.execute("SELECT id, name FROM currency")
    currencies = c.fetchall()

    conn.close()
    return render_template(
        "add_product.html",
        product_types=product_types,
        categories=categories,
        publishers=publishers,
        suppliers=suppliers,
        currencies=currencies
    )
