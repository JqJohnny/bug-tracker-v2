from tests.conftest import make_project, make_token, make_user


# --- Happy path --- #
def test_create_project(client, test_user, auth_headers):
    response = client.post(
        "/api/projects/",
        json={"name": "My Project", "description": "A test project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Project"
    assert data["owner_id"] == str(test_user.id)


def test_get_projects(client, auth_headers):
    client.post("/api/projects/", json={"name": "My Project"}, headers=auth_headers)
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_project(client, test_user, db):
    project = make_project(db, test_user)
    response = client.get(f"/api/projects/{project.id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(project.id)
