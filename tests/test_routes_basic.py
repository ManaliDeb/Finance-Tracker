# tests/test_routes_basic.py

def test_home_route_exists(client):
    response = client.get("/")
    assert response.status_code in (200, 302)


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data.lower()


def test_transactions_route_exists(client):
    response = client.get("/transactions")
    assert response.status_code in (200, 302)


def test_statistics_route_exists(client):
    response = client.get("/statistics")
    assert response.status_code in (200, 302)


def test_missing_page_returns_404(client):
    response = client.get("/this-page-does-not-exist-12345")
    assert response.status_code == 404
