from flask import Blueprint, render_template, redirect, url_for, request, abort
from app import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('', methods=('GET',))
def dashboard():
    db = get_db()
    items = db.execute('SELECT items.id, items.name, items.description, items.price, items.stock, categories.name AS category'
                     ' FROM items JOIN categories ON items.category_id = categories.id'
                     ' ORDER BY items.id').fetchall()
    categories = db.execute('SELECT * FROM categories').fetchall()
    return render_template('admin.html', items=items, categories=categories)

@bp.route('/items/<int:iid>', methods=('POST',))
def update_item(iid):
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (iid,)).fetchone()
    if not item:
        abort(404)
    stock = int(request.form['stock'])
    price = float(request.form['price'])
    db.execute('UPDATE items SET stock = ?, price = ? WHERE id = ?', (stock, price, iid))
    db.commit()
    return redirect(url_for('admin.dashboard'))

@bp.route('/items', methods=('POST',))
def create_item():
    db = get_db()
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    category_id = int(request.form['category_id'])
    db.execute('INSERT INTO items (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)',
              (name, description, price, stock, category_id))
    db.commit()
    return redirect(url_for('admin.dashboard'))

@bp.route('/items/<int:iid>/delete', methods=('POST',))
def delete_item(iid):
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (iid,))
    db.commit()
    return redirect(url_for('admin.dashboard'))

