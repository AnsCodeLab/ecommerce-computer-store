from flask import Blueprint, request, session, redirect, url_for, render_template, abort
from app import get_db

bp = Blueprint("web", __name__)


def _cart_lines(db):
    """Resolve the session cart into display rows + grand total."""
    cart = session.get("cart", {})
    items, total = [], 0.0
    for item_id, quantity in cart.items():
        row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            continue
        line_total = quantity * row["price"]
        total += line_total
        items.append({
            "id": row["id"],
            "name": row["name"],
            "quantity": quantity,
            "price": row["price"],
            "line_total": line_total,
        })
    return items, total


@bp.route("/")
def storefront():
    db = get_db()
    rows = db.execute(
        "SELECT items.*, categories.name AS category "
        "FROM items LEFT JOIN categories ON items.category_id = categories.id "
        "ORDER BY categories.name, items.name"
    ).fetchall()
    # Group items under their category, preserving encounter order.
    categories, index = [], {}
    for row in rows:
        cat = row["category"] or "Uncategorized"
        if cat not in index:
            index[cat] = {"name": cat, "products": []}
            categories.append(index[cat])
        index[cat]["products"].append(row)
    return render_template("index.html", categories=categories)


@bp.route("/item/<int:iid>")
def item_detail(iid):
    db = get_db()
    row = db.execute(
        "SELECT items.*, categories.name AS category "
        "FROM items LEFT JOIN categories ON items.category_id = categories.id "
        "WHERE items.id = ?", (iid,)
    ).fetchone()
    if not row:
        abort(404)
    return render_template("item_detail.html", item=row)


@bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    item_id = request.form["item_id"]
    cart = session.get("cart", {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("web.view_cart"))


@bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    item_id = str(request.form["item_id"])
    cart = session.get("cart", {})
    cart.pop(item_id, None)
    session["cart"] = cart
    return redirect(url_for("web.view_cart"))


@bp.route("/cart")
def view_cart():
    db = get_db()
    items, total = _cart_lines(db)
    return render_template("cart.html", items=items, total=total)


@bp.route("/checkout")
def checkout():
    db = get_db()
    items, total = _cart_lines(db)
    return render_template("checkout.html", items=items, total=total)


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
    order_id = db.execute(
        "INSERT INTO orders (customer_id, status, created_at) VALUES (?, 'confirmed', datetime('now', 'utc'))",
        (customer["id"],)
    ).lastrowid
    total = 0
    for item_id, quantity in cart.items():
        row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            continue
        total += quantity * row["price"]
        db.execute(
            "INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (order_id, item_id, quantity, row["price"])
        )
        db.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (quantity, item_id))
    db.commit()
    session["cart"] = {}
    return render_template("confirmation.html", order_id=order_id, total=total)
