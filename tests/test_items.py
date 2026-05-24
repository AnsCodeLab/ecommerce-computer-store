
def test_create_item(client):
    response = client.post('/api/categories', json={'name': 'Gaming'})
    category = response.get_json()
    category_id = category['id']
    
    response = client.post('/api/items', json={
        'name': 'RTX 4090',
        'description': 'GPU',
        'price': 1599.99,
        'stock': 4,
        'category_id': category_id
    })
    data = response.get_json()
    
    assert response.status_code == 201
    assert 'id' in data
    assert data['name'] == 'RTX 4090'
    assert data['price'] == 1599.99

def test_list_items(client):
    response = client.post('/api/categories', json={'name': 'Gaming'})
    category = response.get_json()
    category_id = category['id']
    
    client.post('/api/items', json={
        'name': 'RTX 4090',
        'description': 'GPU',
        'price': 1599.99,
        'stock': 4,
        'category_id': category_id
    })
    
    client.post('/api/items', json={
        'name': 'RTX 4080',
        'description': 'GPU',
        'price': 1499.99,
        'stock': 3,
        'category_id': category_id
    })
    
    response = client.get('/api/items')
    data = response.get_json()
    
    assert len(data) >= 2

def test_get_item(client):
    response = client.post('/api/categories', json={'name': 'Gaming'})
    category = response.get_json()
    category_id = category['id']
    
    response = client.post('/api/items', json={
        'name': 'RTX 4090',
        'description': 'GPU',
        'price': 1599.99,
        'stock': 4,
        'category_id': category_id
    })
    data = response.get_json()
    item_id = data['id']
    
    response = client.get(f'/api/items/{item_id}')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['id'] == item_id
    assert data['name'] == 'RTX 4090'

def test_get_missing_item(client):
    response = client.get('/api/items/999')
    assert response.status_code == 404

def test_delete_item(client):
    response = client.post('/api/categories', json={'name': 'Gaming'})
    category = response.get_json()
    category_id = category['id']
    
    response = client.post('/api/items', json={
        'name': 'RTX 4090',
        'description': 'GPU',
        'price': 1599.99,
        'stock': 4,
        'category_id': category_id
    })
    data = response.get_json()
    item_id = data['id']
    
    response = client.delete(f'/api/items/{item_id}')
    assert response.status_code == 204
    
    response = client.get(f'/api/items/{item_id}')
    assert response.status_code == 404

