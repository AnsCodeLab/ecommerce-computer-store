from flask import Blueprint, request, jsonify, abort
from app import get_db
import datetime
bp = Blueprint("orders", __name__, url_prefix="/api")

@bp.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    customer_id = data.get("customer_id")
    items = data.get("items", [])

    if not customer_id or not items:
        abort(400)

    db = get_db()

    # Validate every line first (these aborts must propagate, not be swallowed).
    order_items = []
    for item in items:
        item_id = item.get("item_id")
        quantity = item.get("quantity")
        if not item_id or not isinstance(quantity, int) or quantity <= 0:
            abort(400)
        row = db.execute("SELECT price, stock FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            abort(404)
        price, stock = row["price"], row["stock"]
        if stock < quantity:
            abort(400)
        order_items.append((item_id, quantity, price))

    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor = db.execute("INSERT INTO orders (customer_id, status, created_at) VALUES (?, ?, ?)",
                        (customer_id, "confirmed", created_at))
    order_id = cursor.lastrowid
    for item_id, quantity, price in order_items:
        db.execute("INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                   (order_id, item_id, quantity, price))
        db.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (quantity, item_id))
    db.commit()

    total = sum(quantity * price for item_id, quantity, price in order_items)
    return jsonify({
        "id": order_id,
        "customer_id": customer_id,
        "status": "confirmed",
        "created_at": created_at,
        "items": [{"item_id": item_id, "quantity": quantity, "unit_price": price} for item_id, quantity, price in order_items],
        "total": total
    }), 201

@bp.route("/orders", methods=["GET"])
def get_orders():
    db = get_db()
    cursor = db.execute("SELECT * FROM orders")
    orders = [{"id": row[0], "customer_id": row[1], "status": row[2], "created_at": row[3]} for row in cursor]
    return jsonify(orders), 200

@bp.route("/orders/<int:oid>", methods=["GET"])
def get_order(oid):
    db = get_db()
    cursor = db.execute("SELECT * FROM orders WHERE id = ?", (oid,))
    order = cursor.fetchone()
    
    if not order:
        abort(404)
    
    cursor = db.execute("SELECT order_items.item_id, order_items.quantity, order_items.unit_price "
                         "FROM order_items JOIN items ON order_items.item_id = items.id "
                         "WHERE order_items.order_id = ?", (oid,))
    items = [{"item_id": row[0], "quantity": row[1], "unit_price": row[2]} for row in cursor]
    
    total = sum(row["quantity"] * row["unit_price"] for row in items)
    return jsonify({
        "id": order[0],
        "customer_id": order[1],
        "status": order[2],
        "created_at": order[3],
        "items": items,
        "total": total
    }), 200

