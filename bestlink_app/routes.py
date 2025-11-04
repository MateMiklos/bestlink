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

def round_price(price: float) -> float:
    """Round prices to .00 or .50 according to shop rules."""
    base = int(price)
    remainder = price - base

    if remainder == 0:
        return float(price)
    elif remainder <= 0.49:
        return base + 0.50
    else:
        return float(base + 1)

@bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    conn = get_connection()
    c = conn.cursor()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        author = request.form["author"]
        product_type = request.form["product_type"]
        category = request.form["category"]
        publisher = request.form["publisher"]
        supplier = request.form["supplier"]
        publication_date = request.form["publication_date"]
        currency_id = request.form["currency"]
        original_price = float(request.form["original_price"])

        # 1️⃣ Calculate sale price (round up)
        sale_price = round_price(original_price)

        # 2️⃣ Get currency value (conversion rate)
        c.execute("SELECT value FROM currency WHERE id = ?", (currency_id,))
        rate_row = c.fetchone()
        rate = rate_row[0] if rate_row else 1

        # 3️⃣ Calculate price in HUF
        price_in_huf = sale_price * rate

        # 4️⃣ Insert product
        c.execute("""
            INSERT INTO products (
                isbn, product_type, title, author, category, publisher,
                supplier, publication_date, currency, original_price,
                sale_price, price_in_huf
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            isbn, product_type, title, author, category, publisher,
            supplier, publication_date, currency_id, original_price,
            sale_price, price_in_huf
        ))

        # 5️⃣ Initialize stock
        product_id = c.lastrowid
        c.execute("INSERT INTO stock (product_id) VALUES (?)", (product_id,))

        conn.commit()
        conn.close()

        flash(f"✅ Product '{title}' added successfully!", "success")
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
