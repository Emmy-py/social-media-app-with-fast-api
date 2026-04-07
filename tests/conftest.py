# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import settings
from app import schemas
from app.oauth2 import create_access_token
from app import models

# Use PostgreSQL test database
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = schemas.UserResponse(**res.json())
    return {"id": new_user.id, "email": new_user.email, "password": user_data["password"]}


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@example.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = schemas.UserResponse(**res.json())
    return {"id": new_user.id, "email": new_user.email, "password": user_data["password"]}



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user["id"]},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user["id"]},
        {"title": "Third Post", "content": "Content of the third post", "owner_id": test_user["id"]},
        {"title": "Fourth Post", "content": "Content of the fourth post", "owner_id": test_user2["id"]},
    ]
    def create_post_model(post):
        return models.Post(**post)
    post_models = list(map(create_post_model, posts_data))
    session.add_all(post_models)
    session.commit()
    return session.query(models.Post).all()