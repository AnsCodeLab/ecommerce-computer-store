import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
"""

def get_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db(db_path):
    conn = get_conn(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

def seed(db_path):
    conn = get_conn(db_path)
    cursor = conn.cursor()

    # Idempotent: if a catalog already exists, do nothing (re-running run.py is safe).
    if cursor.execute("SELECT COUNT(*) FROM items").fetchone()[0] > 0:
        conn.close()
        return

    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Laptops'), ('Desktops'), ('Components')")
    conn.commit()

    cat = {row["name"]: row["id"] for row in cursor.execute("SELECT id, name FROM categories").fetchall()}

    items = [
        # name, description, price, stock, category
        ("Gaming Laptop 15\"",      "RTX 4060, 16GB RAM, 1TB SSD — high-refresh gaming on the go.", 1299.99, 5,  "Laptops"),
        ("UltraBook Pro 14\"",      "Thin-and-light, 32GB RAM, OLED display, all-day battery.",     1599.99, 8,  "Laptops"),
        ("Budget Notebook 15\"",    "Reliable everyday laptop for browsing, docs, and streaming.",   549.99, 0,  "Laptops"),
        ("Workstation Desktop",     "Ryzen 9, 64GB RAM, RTX 4070 — built for pro workloads.",       2499.99, 3,  "Desktops"),
        ("Compact Mini PC",         "Tiny footprint, big performance. Perfect home-office desktop.", 699.99, 12, "Desktops"),
        ("Gaming Tower RGB",        "Liquid-cooled, RTX 4080, tempered glass with RGB lighting.",   2899.99, 2,  "Desktops"),
        ("1TB NVMe SSD",            "High-speed Gen4 NVMe storage, 7000MB/s reads.",                  89.99, 25, "Components"),
        ("32GB DDR5 RAM Kit",       "6000MHz dual-channel memory kit for modern builds.",            129.99, 18, "Components"),
        ("750W Gold PSU",           "Fully modular 80+ Gold power supply, 10-year warranty.",        109.99, 1,  "Components"),
        ("27\" 1440p 165Hz Monitor", "IPS panel, 1ms response, FreeSync — buttery-smooth visuals.",  329.99, 7,  "Components"),
    ]
    for name, desc, price, stock, category in items:
        cursor.execute(
            "INSERT INTO items (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)",
            (name, desc, price, stock, cat[category]),
        )

    conn.commit()
    conn.close()

