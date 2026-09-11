def test_register(client):
    response = client.post("/api/auth/register", json={
        "name": "New User",
        "email": "newuser@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "password" not in data

