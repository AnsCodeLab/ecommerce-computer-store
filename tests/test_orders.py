import pytest

def test_checkout_creates_order(client):
    # Create category
    response = client.post("/api/categories", json={"name": "Electronics"})
    assert response.status_code == 201
    
    # Create item
    response = client.post("/api/items", json={"name": "Laptop", "description": "High-end laptop", "price": 1000.0, "stock": 5, "category_id": 1})
    assert response.status_code == 201
    item_id = response.get_json()["id"]
    
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 2}]})
    assert response.status_code == 201
    data = response.get_json()
    
    assert data["status"] == "confirmed"
    assert data["total"] == 2000.0
    assert len(data["items"]) == 1

def test_checkout_decrements_stock(client):
    # Create category
    response = client.post("/api/categories", json={"name": "Electronics"})
    assert response.status_code == 201
    
    # Create item
    response = client.post("/api/items", json={"name": "Laptop", "description": "High-end laptop", "price": 1000.0, "stock": 5, "category_id": 1})
    assert response.status_code == 201
    item_id = response.get_json()["id"]
    
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 2}]})
    assert response.status_code == 201
    
    # Check stock
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["stock"] == 3

def test_checkout_insufficient_stock(client):
    # Create category
    response = client.post("/api/categories", json={"name": "Electronics"})
    assert response.status_code == 201
    
    # Create item
    response = client.post("/api/items", json={"name": "Laptop", "description": "High-end laptop", "price": 1000.0, "stock": 1, "category_id": 1})
    assert response.status_code == 201
    item_id = response.get_json()["id"]
    
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 5}]})
    assert response.status_code == 400

def test_checkout_unknown_item(client):
    # Create category
    response = client.post("/api/categories", json={"name": "Electronics"})
    assert response.status_code == 201
    
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": 9999, "quantity": 2}]})
    assert response.status_code == 404

def test_list_orders(client):
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Create item
    response = client.post("/api/items", json={"name": "Laptop", "description": "High-end laptop", "price": 1000.0, "stock": 5})
    assert response.status_code == 201
    item_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 2}]})
    assert response.status_code == 201
    
    # List orders
    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1

def test_get_order(client):
    # Create customer
    response = client.post("/api/customers", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    customer_id = response.get_json()["id"]
    
    # Create item
    response = client.post("/api/items", json={"name": "Laptop", "description": "High-end laptop", "price": 1000.0, "stock": 5})
    assert response.status_code == 201
    item_id = response.get_json()["id"]
    
    # Checkout
    response = client.post("/api/checkout", json={"customer_id": customer_id, "items": [{"item_id": item_id, "quantity": 2}]})
    assert response.status_code == 201
    order_id = response.get_json()["id"]
    
    # Get order
    response = client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert "total" in data

def test_checkout_rejects_negative_quantity(client):
    cat = client.post("/api/categories", json={"name": "C"}).get_json()
    item = client.post("/api/items", json={"name": "X", "price": 10.0, "stock": 5, "category_id": cat["id"]}).get_json()
    cust = client.post("/api/customers", json={"name": "Z", "email": "z@x.com"}).get_json()
    resp = client.post("/api/checkout", json={"customer_id": cust["id"],
                       "items": [{"item_id": item["id"], "quantity": -3}]})
    assert resp.status_code == 400
