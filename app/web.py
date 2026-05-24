from flask import Blueprint, request, session, redirect, url_for, render_template_string, abort
from app import get_db
import datetime

bp = Blueprint("web", __name__)

@bp.route("/")
def storefront():
    db = get_db()
    rows = db.execute("SELECT items.*, categories.name AS category FROM items LEFT JOIN categories ON items.category_id = categories.id").fetchall()
    return render_template_string('''
        <html>
            <head><title>Computer Store</title></head>
            <body>
                <h1>Computer Store</h1>
                <ul>
                    {% for row in rows %}
                    <li>{{ row.name }} - ${{ row.price }} (Stock: {{ row.stock }}) [{{ row.category }}]
                        <form method="POST" action="/cart/add">
                            <input type="hidden" name="item_id" value="{{ row.id }}">
                            <input type="submit" value="Add to cart">
                        </form>
                    </li>
                    {% endfor %}
                </ul>
            </body>
        </html>
    ''', rows=rows)

@bp.route("/item/<int:iid>")
def item_detail(iid):
    db = get_db()
    row = db.execute("SELECT * FROM items WHERE id = ?", (iid,)).fetchone()
    if not row:
        abort(404)
    return render_template_string('''
        <html>
            <head><title>{{ row.name }}</title></head>
            <body>
                <h1>{{ row.name }}</h1>
                <p>{{ row.description }}</p>
                <p>Price: ${{ row.price }}</p>
                <p>Stock: {{ row.stock }}</p>
                <form method="POST" action="/cart/add">
                    <input type="hidden" name="item_id" value="{{ row.id }}">
                    <input type="submit" value="Add to cart">
                </form>
            </body>
        </html>
    ''', row=row)

@bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    item_id = request.form["item_id"]
    cart = session.get("cart", {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("web.view_cart"))

@bp.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    if not cart:
        return render_template_string('''
            <html>
                <body>
                    <h1>Cart</h1>
                    <p>Cart is empty</p>
                    <p><a href="/">Back to store</a></p>
                </body>
            </html>
        ''')
    db = get_db()
    items = []
    total = 0
    for item_id, quantity in cart.items():
        row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if row:
            items.append({
                "name": row["name"],
                "quantity": quantity,
                "price": row["price"],
                "line_total": quantity * row["price"]
            })
            total += quantity * row["price"]
    return render_template_string('''
        <html>
            <body>
                <h1>Cart</h1>
                <ul>
                    {% for item in items %}
                    <li>{{ item.name }} - Quantity: {{ item.quantity }} | Line Total: ${{ item.line_total }}</li>
                    {% endfor %}
                </ul>
                <p><strong>Grand Total: ${{ total }}</strong></p>
                <p><a href="/checkout">Proceed to Checkout</a></p>
                <p><a href="/">Back to store</a></p>
            </body>
        </html>
    ''', items=items, total=total)

@bp.route("/checkout")
def checkout():
    return render_template_string('''
        <html>
            <body>
                <h1>Checkout</h1>
                <form method="POST" action="/checkout">
                    <label>Name: <input type="text" name="name"></label><br>
                    <label>Email: <input type="text" name="email"></label><br>
                    <input type="submit" value="Place Order">
                </form>
                <p><a href="/">Back to store</a></p>
            </body>
        </html>
    ''')

@bp.route("/checkout", methods=["POST"])
def process_checkout():
    name = request.form["name"]
    email = request.form["email"]
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("web.view_cart"))
    db = get_db()
    db.execute("INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)", (name, email))
    customer = db.execute("SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
    if not customer:
        abort(400, "Customer not found")
    order_id = db.execute("INSERT INTO orders (customer_id, status, created_at) VALUES (?, 'confirmed', datetime('now', 'utc'))", (customer["id"],)).lastrowid
    total = 0
    for item_id, quantity in cart.items():
        row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            continue
        total += quantity * row["price"]
        db.execute("INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, item_id, quantity, row["price"]))
        db.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (quantity, item_id))
    db.commit()
    session["cart"] = {}
    return render_template_string('''
        <html>
            <body>
                <h1>Order Confirmation</h1>
                <p>Order ID: {{ order_id }}</p>
                <p>Total: ${{ total }}</p>
                <p>Thank you for your purchase!</p>
                <p><a href="/">Back to store</a></p>
            </body>
        </html>
    ''', order_id=order_id, total=total)

