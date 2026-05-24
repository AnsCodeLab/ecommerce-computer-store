from flask import Blueprint, request, jsonify, abort
from app import get_db
bp = Blueprint("categories", __name__, url_prefix="/api/categories")

@bp.route('', methods=['GET'])
def get_categories():
    db = get_db()
    cur = db.execute('SELECT id, name FROM categories')
    categories = [dict(row) for row in cur.fetchall()]
    return jsonify(categories), 200

@bp.route('/<int:cid>', methods=['GET'])
def get_category(cid):
    db = get_db()
    cur = db.execute('SELECT id, name FROM categories WHERE id = ?', (cid,))
    row = cur.fetchone()
    if row is None:
        abort(404)
    return jsonify(dict(row)), 200

@bp.route('', methods=['POST'])
def create_category():
    db = get_db()
    name = request.json['name']
    cur = db.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    db.commit()
    new_id = cur.lastrowid
    return jsonify(dict(db.execute('SELECT id, name FROM categories WHERE id = ?', (new_id,)).fetchone())), 201

@bp.route('/<int:cid>', methods=['DELETE'])
def delete_category(cid):
    db = get_db()
    cur = db.execute('SELECT id, name FROM categories WHERE id = ?', (cid,))
    row = cur.fetchone()
    if row is None:
        abort(404)
    db.execute('DELETE FROM categories WHERE id = ?', (cid,))
    db.commit()
    return '', 204

