import pytest

from tests.conftest import make_user

# --- Happy path --- #


def test_register(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "password" not in data


def test_login(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Login Test",
            "email": "logintest@example.com",
            "password": "securepassword123",
        },
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "logintest@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


# --- Auth failures --- #


def test_login_invalid_password(client, db):
    make_user(db, "newuser@example.com")
    response = client.post(
        "/api/auth/login",
        data={
            "username": "newuser@example.com",
            "password": "invalidpassword",
        },
    )
    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_login_nonexistent_email(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "doesnotexist@example.com", "password": "somepassword"},
    )
    assert response.status_code == 401


# --- Invalid input --- #


def test_duplicate_email(client, db):
    make_user(db, "newuser@example.com")
    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.parametrize(
    "payload, missing_field",
    [
        ({"email": "test@example.com", "password": "securepassword123"}, "name"),
        ({"name": "Test User", "password": "securepassword123"}, "email"),
        ({"name": "Test User", "email": "test@example.com"}, "password"),
    ],
)
def test_register_missing_fields(client, payload, missing_field):
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 422, f"expected 422 when {missing_field} is missing"


@pytest.mark.parametrize(
    "bad_email",
    [
        "notanemail",
        "missing@domain",
        "@nodomain.com",
        "spaces in@email.com",
        "double@@at.com",
    ],
)
def test_register_invalid_email(client, bad_email):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": bad_email, "password": "securepassword123"},
    )
    assert response.status_code == 422