# tests/test_routes_basic.py

def test_home_route_exists(client):
    """
    The home page ('/') should exist.
    It might redirect (302) if the user is not logged in, or return 200.
    """
    response = client.get("/")
    assert response.status_code in (200, 302)


def test_login_page_loads(client):
    """
    The login page should load with status 200 and contain the word 'login'.
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_page_loads(client):
    """
    The registration page should load with status 200 and contain the word 'register'.
    """
    response = client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data.lower()


def test_transactions_route_exists(client):
    """
    The /transactions page should exist.
    It may be protected and redirect (302), or return 200 if public.
    """
    response = client.get("/transactions")
    assert response.status_code in (200, 302)


def test_statistics_route_exists(client):
    """
    The /statistics page should exist.
    It may be protected and redirect (302), or return 200 if public.
    """
    response = client.get("/statistics")
    assert response.status_code in (200, 302)


def test_missing_page_returns_404(client):
    """
    A clearly invalid URL should return 404.
    """
    response = client.get("/this-page-does-not-exist-12345")
    assert response.status_code == 404
