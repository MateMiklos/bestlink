import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "instance", "bestlink.db")

def get_connection():
    """Create and return a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_product_type_table():
    """Create the product_type table with fixed data."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS product_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    product_types = [
        ("Paperback",),
        ("Hardback",),
        ("Trade Paperback",),
        ("Pocket",),
        ("Bookmark",),
        ("Totebag",),
        ("Puzzle",),
        ("Card",)
    ]

    c.executemany("INSERT OR IGNORE INTO product_type (name) VALUES (?)", product_types)
    conn.commit()
    conn.close()

def create_currency_table():
    """Create the currency table with fixed data."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            symbol TEXT
        )
    """)

    currencies = [
        ("Euro", "€"),
        ("Pound Sterling", "£"),
        ("US Dollar", "$"),
        ("Hungarian Forint", "Ft")
    ]

    c.executemany("INSERT OR IGNORE INTO currency (name, symbol) VALUES (?, ?)", currencies)
    conn.commit()
    conn.close()

def create_categories_table():
    """Create the categories table with fixed data."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    categories = [
        ("Fiction",),
        ("Classic Fiction",),
        ("Crime Fiction",),
        ("Romantic Fiction",),
        ("Young Adult Fiction",),
        ("Other",)
    ]

    c.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", categories)
    conn.commit()
    conn.close()

def create_publishers_table():
    """Create the publishers table (can be expanded later)."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    publishers = [
        ("Penguin Books",),
        ("HarperCollins",),
        ("Simon & Schuster",),
        ("Macmillan",),
        ("Oxford University Press",)
    ]

    c.executemany("INSERT OR IGNORE INTO publishers (name) VALUES (?)", publishers)
    conn.commit()
    conn.close()

def create_suppliers_table():
    """Create the suppliers table (can be expanded later)."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    suppliers = [
        ("Gardners",),
        ("Ingram",)
    ]

    c.executemany("INSERT OR IGNORE INTO suppliers (name) VALUES (?)", suppliers)
    conn.commit()
    conn.close()

def create_products_table():
    """Create the products table if it doesn’t exist."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT,
            product_type INTEGER,
            title TEXT NOT NULL,
            author TEXT,
            category INTEGER,
            publisher INTEGER,
            supplier INTEGER,
            publication_date TEXT,
            currency INTEGER,
            original_price REAL,
            sale_price REAL,
            price_in_huf REAL,
            FOREIGN KEY (product_type) REFERENCES product_type(id),
            FOREIGN KEY (category) REFERENCES categories(id),
            FOREIGN KEY (publisher) REFERENCES publishers(id),
            FOREIGN KEY (supplier) REFERENCES suppliers(id),
            FOREIGN KEY (currency) REFERENCES currency(id)
        )
    """)

    conn.commit()
    conn.close()

def init_db():
    """Initialize all database tables."""
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "instance"), exist_ok=True)
    create_product_type_table()
    create_currency_table()
    create_categories_table()
    create_publishers_table()
    create_suppliers_table()
    create_products_table()

