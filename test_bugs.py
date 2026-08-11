import pytest
from app.models import User, Project
from app.auth import hash_password, create_access_token


def make_user(db, email: str, name: str = "Test User") -> User:
    user = User(name=name, email=email, password=hash_password("testpassword123"))
    db.add(user)
    db.flush()
    return user


def make_project(db, owner) -> Project:
    project = Project(name="Test Project", owner_id=owner.id)
    db.add(project)
    db.flush()
    return project


def make_token(user: User) -> dict:
    token = create_access_token(data={"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}