from flask import Blueprint, request, abort
from app import get_db

bp = Blueprint('items', __name__, url_prefix='/api/items')

@bp.route('', methods=['GET'])
def get_items():
    db = get_db()
    cur = db.execute('SELECT * FROM items')
    return [dict(row) for row in cur.fetchall()]

@bp.route('/<int:iid>', methods=['GET'])
def get_item(iid):
    db = get_db()
    cur = db.execute('SELECT * FROM items WHERE id = ?', (iid,))
    row = cur.fetchone()
    if row is None:
        abort(404)
    return dict(row)

@bp.route('', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data['name']
    description = data.get('description')
    price = data['price']
    stock = data.get('stock', 0)
    category_id = data.get('category_id')
    
    db = get_db()
    cur = db.execute('INSERT INTO items (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)',
                     (name, description, price, stock, category_id))
    db.commit()
    new_id = cur.lastrowid
    
    cur = db.execute('SELECT * FROM items WHERE id = ?', (new_id,))
    return dict(cur.fetchone()), 201

@bp.route('/<int:iid>', methods=['DELETE'])
def delete_item(iid):
    db = get_db()
    cur = db.execute('DELETE FROM items WHERE id = ?', (iid,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return '', 204

