import pytest
from app import db
from app.models import User
from argon2 import PasswordHasher

# Create a test user with valid hashed password
@pytest.fixture
def new_user(app):
    ph = PasswordHasher()
    user = User(email="test123@example.com", password=ph.hash("Password1*"))
    db.session.add(user)
    db.session.commit()
    return user

# Test homepage shows correct content when not logged in
def test_home_route_unauthenticated(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Test homepage redirects to dashboard if logged in
def test_home_route_authenticated(client, new_user):
    with client.session_transaction() as sess:
        sess["user_id"] = new_user.id

    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]

# Test login page renders correctly
def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

# Test login with valid credentials
def test_login_valid_credentials(client, new_user):
    response = client.post("/login", data={
        "email": "test123@example.com",
        "password": "Password1*"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your PDF Assistant" in response.data
    with client.session_transaction() as sess:
        assert "user_id" in sess

# Test login fails with wrong password
def test_login_invalid_password(client, new_user):
    response = client.post("/login", data={
        "email": "test123@example.com",
        "password": "Password1*#"
    }, follow_redirects=True)
    assert b"Invalid credentials." in response.data

# Test login with nonexistent email
def test_login_nonexistent_user(client):
    response = client.post("/login", data={
        "email": "notfound@example.com",
        "password": "Password1*#"
    }, follow_redirects=True)
    assert b"No user found with this email." in response.data

# Test sign-up page renders
def test_signup_page_renders(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Sign Up" in response.data in response.data

# Test successful signup flow
def test_signup_success(client):
    response = client.post("/signup", data={
        "email": "newuser@example.com",
        "password": "Passw*rd1#"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your PDF Assistant" in response.data

# Test error on duplicate email during sign-up
def test_signup_duplicate_email(client, new_user):
    response = client.post("/signup", data={
        "email": "test123@example.com",
        "password": "Passw*rd1"
    }, follow_redirects=True)
    assert b"Email already registered." in response.data

# Test logout clears session and redirects
def test_logout_clears_session(client, new_user):
    with client.session_transaction() as sess:
        sess["user_id"] = new_user.id

    response = client.get("/logout", follow_redirects=True)
    assert response.request.path == "/"
    with client.session_transaction() as sess:
        assert "user_id" not in sess