from tests.conftest import make_project, make_token, make_user

# --- Happy path --- #


def test_create_bug(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    response = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test bug"
    assert data["author_id"] == str(test_user.id)


def test_get_bugs(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    response = client.get("/api/bugs/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_bug_as_author(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.patch(
        f"/api/bugs/{bug_id}", json={"title": "Updated title"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_update_bug_as_assignee(client, test_user, auth_headers, db):
    assignee = make_user(db, "assignee@example.com")
    assignee_headers = make_token(assignee)
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={
            "title": "Test bug",
            "project_id": str(project.id),
            "assignee_id": str(assignee.id),
        },
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.patch(
        f"/api/bugs/{bug_id}",
        json={"title": "Assignee updated"},
        headers=assignee_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Assignee updated"


def test_delete_bug_as_author(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.delete(f"/api/bugs/{bug_id}", headers=auth_headers)
    assert response.status_code == 204


# --- Auth / ownership checks --- #


def test_create_bug_unauthenticated(client, db, test_user):
    project = make_project(db, test_user)
    response = client.post(
        "/api/bugs/", json={"title": "Test bug", "project_id": str(project.id)}
    )
    assert response.status_code == 401


def test_update_bug_as_unrelated_user(client, test_user, auth_headers, db):
    other_user = make_user(db, "other@example.com")
    other_headers = make_token(other_user)
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.patch(
        f"/api/bugs/{bug_id}", json={"title": "Should fail"}, headers=other_headers
    )
    assert response.status_code == 403


def test_delete_bug_as_non_author(client, test_user, auth_headers, db):
    other_user = make_user(db, "nonauthor@example.com")
    other_headers = make_token(other_user)
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.delete(f"/api/bugs/{bug_id}", headers=other_headers)
    assert response.status_code == 403


# --- Invalid input --- #


def test_create_bug_missing_title(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    response = client.post(
        "/api/bugs/", json={"project_id": str(project.id)}, headers=auth_headers
    )
    assert response.status_code == 422


def test_create_bug_missing_project_id(client, test_user, auth_headers):
    response = client.post(
        "/api/bugs/", json={"title": "Test bug"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_create_bug_invalid_priority(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    response = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id), "priority": "urgent"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_update_bug_invalid_status(client, test_user, auth_headers, db):
    project = make_project(db, test_user)
    create = client.post(
        "/api/bugs/",
        json={"title": "Test bug", "project_id": str(project.id)},
        headers=auth_headers,
    )
    bug_id = create.json()["id"]
    response = client.patch(
        f"/api/bugs/{bug_id}", json={"status": "deleted"}, headers=auth_headers
    )
    assert response.status_code == 422
