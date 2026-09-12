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
