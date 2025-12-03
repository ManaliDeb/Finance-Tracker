# few basic route tests


def test_home_route_exists(client):
    """
    The home page ('/') should exist.
    In many finance apps, if the user is not logged in, this might redirect.
    We accept 200 (OK) or 302 (Redirect).
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
    If it is protected, it may redirect (302) when not logged in.
    """
    response = client.get("/transactions")
    assert response.status_code in (200, 302)


def test_statistics_route_exists(client):
    """
    The /statistics page should exist.
    It may be protected (302) or public (200).
    """
    response = client.get("/statistics")
    assert response.status_code in (200, 302)


def test_missing_page_returns_404(client):
    """
    A clearly invalid URL should return 404.
    """
    response = client.get("/this-page-does-not-exist-12345")
    assert response.status_code == 404