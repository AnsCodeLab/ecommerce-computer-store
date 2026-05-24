ADMIN_PW = "admin"  # default test password (create_app reads ADMIN_PASSWORD env, defaults to this)


def _seed_item(client, name='RTX 4090', stock=4, price=1599.99):
    cid = client.post('/api/categories', json={'name': 'Gaming'}).get_json()['id']
    return client.post('/api/items', json={
        'name': name, 'description': 'GPU', 'price': price,
        'stock': stock, 'category_id': cid,
    }).get_json()['id']


def _login(client, password=ADMIN_PW):
    return client.post('/admin/login', data={'password': password}, follow_redirects=True)


# ---- auth gate ----

def test_admin_requires_login(client):
    resp = client.get('/admin')
    assert resp.status_code == 302
    assert '/admin/login' in resp.headers['Location']


def test_admin_login_page_renders(client):
    assert client.get('/admin/login').status_code == 200


def test_admin_login_wrong_password_denied(client):
    client.post('/admin/login', data={'password': 'nope'})
    # still gated
    assert client.get('/admin').status_code == 302


def test_admin_login_success_grants_access(client):
    _login(client)
    assert client.get('/admin').status_code == 200


def test_admin_action_requires_login(client):
    iid = _seed_item(client)
    resp = client.post(f'/admin/items/{iid}', data={'stock': '5', 'price': '1'})
    assert resp.status_code == 302
    assert '/admin/login' in resp.headers['Location']
    # stock unchanged
    assert client.get(f'/api/items/{iid}').get_json()['stock'] == 4


def test_admin_logout(client):
    _login(client)
    assert client.get('/admin').status_code == 200
    client.get('/admin/logout')
    assert client.get('/admin').status_code == 302


# ---- functionality (now behind login) ----

def test_admin_lists_items(client):
    _seed_item(client)
    _login(client)
    resp = client.get('/admin')
    assert resp.status_code == 200
    assert b'RTX 4090' in resp.data


def test_admin_update_stock(client):
    iid = _seed_item(client, stock=4)
    _login(client)
    resp = client.post(f'/admin/items/{iid}', data={'stock': '30', 'price': '1599.99'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert client.get(f'/api/items/{iid}').get_json()['stock'] == 30


def test_admin_add_item(client):
    cid = client.post('/api/categories', json={'name': 'Gaming'}).get_json()['id']
    _login(client)
    resp = client.post('/admin/items', data={
        'name': 'New GPU', 'description': 'fast', 'price': '999.99',
        'stock': '7', 'category_id': str(cid),
    }, follow_redirects=True)
    assert resp.status_code == 200
    names = [i['name'] for i in client.get('/api/items').get_json()]
    assert 'New GPU' in names


def test_admin_delete_item(client):
    iid = _seed_item(client)
    _login(client)
    resp = client.post(f'/admin/items/{iid}/delete', follow_redirects=True)
    assert resp.status_code == 200
    assert client.get(f'/api/items/{iid}').status_code == 404
