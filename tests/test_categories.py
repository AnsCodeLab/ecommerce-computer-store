def test_create_category(client):
    response = client.post("/api/categories", json={"name": "GPUs"})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'GPUs'


def test_list_categories(client):
    client.post("/api/categories", json={"name": "GPUs"})
    client.post("/api/categories", json={"name": "CPUs"})
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert len(response.get_json()) >= 2


def test_get_category(client):
    created = client.post("/api/categories", json={"name": "GPUs"}).get_json()
    response = client.get(f"/api/categories/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()['name'] == 'GPUs'


def test_get_missing_category(client):
    assert client.get("/api/categories/9999").status_code == 404


def test_delete_category(client):
    cid = client.post("/api/categories", json={"name": "GPUs"}).get_json()['id']
    assert client.delete(f"/api/categories/{cid}").status_code == 204
    assert client.get(f"/api/categories/{cid}").status_code == 404
