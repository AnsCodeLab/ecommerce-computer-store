
def test_create_customer(client):
    response = client.post('/api/customers', json={'name': 'Ada', 'email': 'ada@x.com'})
    data = response.get_json()
    
    assert response.status_code == 201
    assert 'id' in data
    assert data['email'] == 'ada@x.com'

def test_list_customers(client):
    client.post('/api/customers', json={'name': 'Ada', 'email': 'ada@x.com'})
    client.post('/api/customers', json={'name': 'Bob', 'email': 'bob@x.com'})
    
    response = client.get('/api/customers')
    data = response.get_json()
    
    assert len(data) >= 2

def test_get_customer(client):
    response = client.post('/api/customers', json={'name': 'Ada', 'email': 'ada@x.com'})
    data = response.get_json()
    customer_id = data['id']
    
    response = client.get(f'/api/customers/{customer_id}')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['id'] == customer_id
    assert data['name'] == 'Ada'

def test_get_missing_customer(client):
    response = client.get('/api/customers/999')
    assert response.status_code == 404

def test_delete_customer(client):
    response = client.post('/api/customers', json={'name': 'Ada', 'email': 'ada@x.com'})
    data = response.get_json()
    customer_id = data['id']
    
    response = client.delete(f'/api/customers/{customer_id}')
    assert response.status_code == 204
    
    response = client.get(f'/api/customers/{customer_id}')
    assert response.status_code == 404