```markdown
# 2026-05-24 E-commerce Store TDD Plan

## Task 1: Define and Initialize Database Schema

### Write failing test(s)
```python
def test_db_schema_not_initialized(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "categories" in tables
        assert "items" in tables
        assert "customers" in tables
        assert "orders" in tables
        assert "order_items" in tables
```

### Implement
```python
# app/db.py
SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
"""

def get_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path):
    with get_conn(db_path) as conn:
        conn.executescript(SCHEMA)

def seed(db_path):
    with get_conn(db_path) as conn:
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Laptops')")
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Desktops')")
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Components')")
        conn.execute("INSERT OR IGNORE INTO items (category_id, name, price, stock) VALUES (1, 'MacBook Pro', 1999.99, 5)")
        conn.execute("INSERT OR IGNORE INTO items (category_id, name, price, stock) VALUES (1, 'Dell XPS', 1499.99, 3)")
        conn.execute("INSERT OR IGNORE INTO items (category_id, name, price, stock) VALUES (2, 'Dell Optiplex', 899.99, 2)")
        conn.execute("INSERT OR IGNORE INTO items (category_id, name, price, stock) VALUES (3, 'SSD 1TB', 49.99, 10)")
        conn.execute("INSERT OR IGNORE INTO items (category_id, name, price, stock) VALUES (3, 'RAM 16GB', 89.99, 5)")
```

## Task 2: Create Flask App and Register Blueprints

### Write failing test(s)
```python
def test_app_creates_db_and_registers_blueprints(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "categories" in tables
        assert "items" in tables
        assert "customers" in tables
        assert "orders" in tables
        assert "order_items" in tables
```

## Task 3: Implement Categories Blueprint

### Write failing test(s)
```python
def test_get_categories_returns_empty_list(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_post_category_returns_201(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.post("/api/categories", json={"name": "Test Category"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["name"] == "Test Category"
```

### Implement
```python
# app/categories.py
from flask import Blueprint, request, jsonify

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/api/categories', methods=['GET'])
def get_categories():
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = [dict(row) for row in cursor.fetchall()]
    return jsonify(categories)

@categories_bp.route('/api/categories', methods=['POST'])
def create_category():
    from app import get_db
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    db.commit()
    cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
    category = cursor.fetchone()
    return jsonify(dict(category)), 201
```

## Task 4: Implement Items Blueprint

### Write failing test(s)
```python
def test_get_items_returns_empty_list(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_post_item_returns_201(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.post("/api/items", json={"category_id": 1, "name": "Test Item", "price": 100.00, "stock": 5})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["category_id"] == 1
    assert data["name"] == "Test Item"
    assert data["price"] == 100.00
    assert data["stock"] == 5
```

### Implement
```python
# app/items.py
from flask import Blueprint, request, jsonify

items_bp = Blueprint('items', __name__)

@items_bp.route('/api/items', methods=['GET'])
def get_items():
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM items")
    items = [dict(row) for row in cursor.fetchall()]
    return jsonify(items)

@items_bp.route('/api/items', methods=['POST'])
def create_item():
    from app import get_db
    data = request.get_json()
    category_id = data.get('category_id')
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    if not all([category_id, name, price, stock]):
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO items (category_id, name, price, stock) VALUES (?, ?, ?, ?)", 
                   (category_id, name, price, stock))
    db.commit()
    cursor.execute("SELECT * FROM items WHERE id = ?", (cursor.lastrowid,))
    item = cursor.fetchone()
    return jsonify(dict(item)), 201
```

## Task 5: Implement Customers Blueprint

### Write failing test(s)
```python
def test_get_customers_returns_empty_list(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.get("/api/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_post_customer_returns_201(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
```

### Implement
```python
# app/customers.py
from flask import Blueprint, request, jsonify

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/api/customers', methods=['GET'])
def get_customers():
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = [dict(row) for row in cursor.fetchall()]
    return jsonify(customers)

@customers_bp.route('/api/customers', methods=['POST'])
def create_customer():
    from app import get_db
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not all([name, email]):
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (cursor.lastrowid,))
    customer = cursor.fetchone()
    return jsonify(dict(customer)), 201
```

## Task 6: Implement Orders Blueprint

### Write failing test(s)
```python
def test_post_checkout_returns_201(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    # Seed data
    with app.app_context():
        from app import get_db
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO customers (name, email) VALUES ('Alice', 'alice@example.com')")
        db.commit()
        cursor.execute("SELECT id FROM customers WHERE name = 'Alice'")
        customer_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO items (category_id, name, price, stock) VALUES (1, 'Laptop', 1000.00, 1)")
        db.commit()
        cursor.execute("SELECT id FROM items WHERE name = 'Laptop'")
        item_id = cursor.fetchone()[0]
    # Test checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 1}]})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["customer_id"] == customer_id
    assert data["status"] == "confirmed"
    assert data["created_at"] is not None
    assert data["line_items"] == [{"item_id": item_id, "quantity": 1, "unit_price": 1000.00}]
    assert data["total"] == 1000.00
```

### Implement
```python
# app/orders.py
from flask import Blueprint, request, jsonify
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/checkout', methods=['POST'])
def checkout():
    from app import get_db
    data = request.get_json()
    customer_id = data.get('customer_id')
    items = data.get('items')
    if not all([customer_id, items]):
        return jsonify({'error': 'Missing fields'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    for item in items:
        item_id = item.get('item_id')
        quantity = item.get('quantity')
        if not all([item_id, quantity]):
            return jsonify({'error': 'Missing item fields'}), 400
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        if item['stock'] < quantity:
            return jsonify({'error': 'Not enough stock'}), 400
        cursor.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (quantity, item_id))
        db.commit()
    cursor.execute("INSERT INTO orders (customer_id, status, created_at) VALUES (?, 'confirmed', ?)", 
                  (customer_id, datetime.now()))
    order_id = cursor.lastrowid
    db.commit()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    line_items = []
    for item in items:
        item_id = item.get('item_id')
        quantity = item.get('quantity')
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        line_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'unit_price': item['price']
        })
    cursor.execute("INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", 
                  (order_id, item_id, quantity, item['price']))
    db.commit()
    return jsonify({
        'id': order['id'],
        'customer_id': order['customer_id'],
        'status': order['status'],
        'created_at': order['created_at'],
        'line_items': line_items,
        'total': sum(item['unit_price'] * item['quantity'] for item in line_items)
    }), 201

@orders_bp.route('/api/orders', methods=['GET'])
def get_orders():
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = [dict(row) for row in cursor.fetchall()]
    return jsonify(orders)

@orders_bp.route('/api/orders/<int:id>', methods=['GET'])
def get_order(id):
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    order = cursor.fetchone()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(dict(order))
```

## Task 7: Implement Web Blueprint

### Write failing test(s)
```python
def test_web_home_returns_html(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(db_path)
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Storefront" in response.data.decode('utf-8')
```

### Implement
```python
# app/web.py
from flask import Blueprint, render_template, redirect, url_for, request, session

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    from app import get_db
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = [dict(row) for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM items")
   