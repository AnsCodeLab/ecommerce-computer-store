import pytest
from app.db import seed, get_conn, init_db


def test_init_db_creates_tables(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    conn = get_conn(db_path)
    names = {row["name"] for row in
             conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    conn.close()
    for expected in ["categories", "items", "customers", "orders", "order_items"]:
        assert expected in names


def test_seed_inserts_data(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    seed(db_path)
    conn = get_conn(db_path)
    assert conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 3
    assert conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] >= 3
    names = {row["name"] for row in conn.execute("SELECT name FROM items").fetchall()}
    conn.close()
    assert {"Gaming Laptop", "Workstation Desktop", "SSD Storage"} <= names
