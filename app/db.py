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
    
    # Insert categories
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Laptops'), ('Desktops'), ('Components')")
    conn.commit()
    
    # Insert items
    cursor.execute("SELECT id FROM categories WHERE name = 'Laptops'")
    laptop_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM categories WHERE name = 'Desktops'")
    desktop_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM categories WHERE name = 'Components'")
    component_id = cursor.fetchone()[0]
    
    # Insert sample items
    cursor.execute("INSERT OR IGNORE INTO items (name, description, price, stock, category_id) VALUES ('Gaming Laptop', 'High-performance gaming laptop', 1299.99, 5, ?)", (laptop_id,))
    cursor.execute("INSERT OR IGNORE INTO items (name, description, price, stock, category_id) VALUES ('Workstation Desktop', 'Powerful desktop for professional work', 2499.99, 3, ?)", (desktop_id,))
    cursor.execute("INSERT OR IGNORE INTO items (name, description, price, stock, category_id) VALUES ('SSD Storage', 'High-speed SSD storage', 89.99, 10, ?)", (component_id,))
    
    conn.commit()
    conn.close()

