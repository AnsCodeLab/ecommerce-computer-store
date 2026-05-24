from flask import Blueprint, request, abort
from app import get_db

bp = Blueprint('customers', __name__, url_prefix='/api/customers')

@bp.route('', methods=['GET'])
def get_customers():
    db = get_db()
    cur = db.execute('SELECT * FROM customers')
    return [dict(row) for row in cur.fetchall()]

@bp.route('/<int:cid>', methods=['GET'])
def get_customer(cid):
    db = get_db()
    cur = db.execute('SELECT * FROM customers WHERE id = ?', (cid,))
    row = cur.fetchone()
    if row is None:
        abort(404)
    return dict(row)

@bp.route('', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data['name']
    email = data['email']
    
    db = get_db()
    cur = db.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
    db.commit()
    new_id = cur.lastrowid
    
    cur = db.execute('SELECT * FROM customers WHERE id = ?', (new_id,))
    return dict(cur.fetchone()), 201

@bp.route('/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    db = get_db()
    cur = db.execute('DELETE FROM customers WHERE id = ?', (cid,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return '', 204

