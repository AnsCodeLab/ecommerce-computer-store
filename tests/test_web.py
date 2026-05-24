def _make_item(client, name="RTX 4090", price=1599.99, stock=3):
    cid = client.post("/api/categories", json={"name": "GPUs"}).get_json()["id"]
    return client.post("/api/items", json={
        "name": name, "description": "fast", "price": price,
        "stock": stock, "category_id": cid,
    }).get_json()["id"]


def test_storefront_lists_items(client):
    _make_item(client)
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"RTX 4090" in resp.data


def test_item_detail(client):
    iid = _make_item(client)
    resp = client.get(f"/item/{iid}")
    assert resp.status_code == 200
    assert b"RTX 4090" in resp.data


def test_item_detail_missing(client):
    assert client.get("/item/9999").status_code == 404


def test_add_to_cart_and_view(client):
    iid = _make_item(client)
    resp = client.post("/cart/add", data={"item_id": iid}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"RTX 4090" in resp.data


def test_web_checkout_creates_order(client):
    iid = _make_item(client, stock=5)
    client.post("/cart/add", data={"item_id": iid})
    resp = client.post("/checkout", data={"name": "Ada", "email": "ada@x.com"},
                       follow_redirects=True)
    assert resp.status_code == 200
    orders = client.get("/api/orders").get_json()
    assert len(orders) >= 1
