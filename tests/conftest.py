import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import create_access_token, hash_password
from app.database import Base, get_db
from app.main import app
from app.models import Bug, PriorityEnum, Project, StatusEnum, User

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db):
    user = User(
        name="Test User",
        email="test@example.com",
        password=hash_password("testpassword123"),
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def auth_token(test_user):
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture()
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


def make_bug(db, author, project, **kwargs) -> Bug:
    bug = Bug(
        title=kwargs.get("title", "Test Bug"),
        author_id=author.id,
        project_id=project.id,
        status=kwargs.get("status", StatusEnum.open),
        priority=kwargs.get("priority", PriorityEnum.low),
        assignee_id=kwargs.get("assignee_id"),
    )
    db.add(bug)
    db.flush()
    return bug


def make_user(db, email: str, name: str = "Test User") -> User:
    user = User(
        name=name,
        email=email,
        password=hash_password("testpassword123"),
    )
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
