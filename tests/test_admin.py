def _seed_item(client, name='RTX 4090', stock=4, price=1599.99):
    cid = client.post('/api/categories', json={'name': 'Gaming'}).get_json()['id']
    return client.post('/api/items', json={
        'name': name, 'description': 'GPU', 'price': price,
        'stock': stock, 'category_id': cid,
    }).get_json()['id']


def test_admin_lists_items(client):
    _seed_item(client)
    resp = client.get('/admin')
    assert resp.status_code == 200
    assert b'RTX 4090' in resp.data


def test_admin_update_stock(client):
    iid = _seed_item(client, stock=4)
    resp = client.post(f'/admin/items/{iid}', data={'stock': '30', 'price': '1599.99'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert client.get(f'/api/items/{iid}').get_json()['stock'] == 30


def test_admin_add_item(client):
    cid = client.post('/api/categories', json={'name': 'Gaming'}).get_json()['id']
    resp = client.post('/admin/items', data={
        'name': 'New GPU', 'description': 'fast', 'price': '999.99',
        'stock': '7', 'category_id': str(cid),
    }, follow_redirects=True)
    assert resp.status_code == 200
    names = [i['name'] for i in client.get('/api/items').get_json()]
    assert 'New GPU' in names


def test_admin_delete_item(client):
    iid = _seed_item(client)
    resp = client.post(f'/admin/items/{iid}/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert client.get(f'/api/items/{iid}').status_code == 404
