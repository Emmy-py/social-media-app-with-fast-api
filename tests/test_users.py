from app import schemas
from .conftest import client, session
import pytest
from jose import jwt
from app.config import settings
from .conftest import test_user



# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World!"}

# def test_create_users(client):
#     res = client.post("/users/", json={"email": "test4@example.com", "password": "password123"})
#     new_user = schemas.UserResponse(**res.json())
#     assert res.status_code == 201
#     assert new_user.email == "test4@example.com"


# def test_login_user(client):
#     res = client.post("/login", data={"username": "test4@example.com", "password": "password123"})
#     assert res.status_code == 200
#     assert "access_token" in res.json()
#     assert res.json()["token_type"] == "bearer"



def test_create_user(client):
    res = client.post("/users/", json={"email":"test5@example.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test5@example.com"

def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, 
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id is not None
    assert id == test_user["id"]
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert login_res.token_type == "bearer"
