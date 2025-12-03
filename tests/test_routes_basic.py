# tests/test_routes_basic.py

def test_home_route_exists(client):
    # Basic check: the home page ('/') should exist.
    # If the user is not logged in, it usually redirects to /login (302)
    response = client.get("/")
    # send a GET request to "/"
    # Accept either 200 (OK) or 302 (Redirect)
    assert response.status_code in (200, 302)


def test_login_page_loads(client):    #Basic check: the login page should load correctly.

    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_page_loads(client):
    #  Basic check: the registration page should load correctly.

    response = client.get("/register")
    assert response.status_code == 200 # page loads OK
    # Page content should contain the word "login" somewhere
    assert b"register" in response.data.lower()

def test_transactions_route_exists(client):
    #Basic check: /transactions should exist.
    #For logged-out users, it may redirect to /login.
    response = client.get("/transactions")
    assert response.status_code in (200, 302)


def test_statistics_route_exists(client):
    # /statistics should exist. It may be protected (redirect) or public
    response = client.get("/statistics")
    assert response.status_code in (200, 302)


def test_missing_page_returns_404(client):
    #case: a clearly invalid URL should return 404.
    response = client.get("/this-page-does-not-exist-12345")
    assert response.status_code == 404

def test_transactions_redirects_when_not_logged_in(client):
    #Edge case: if a user is not logged in and tries to access /transactions,
    #the app should redirect them (usually to /login).

    response = client.get("/transactions", follow_redirects=False)
    assert response.status_code == 302  # redirect expected


def test_login_with_empty_form_shows_error_or_stays_on_page(client):
    #Edge case: submitting the login form with no data should NOT log the user in.
    #We at least expect to stay on the login page (200) instead of crashing.
    
    response = client.post("/login", data={"username": "", "password": ""})
    assert response.status_code == 200

