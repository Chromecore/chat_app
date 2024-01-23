from fastapi.testclient import TestClient
from backend.main import app

def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_create_user():
    pass

def test_get_user_by_id():
    pass

def test_get_user_invalid_id():
    pass

def test_get_users_chats():
    pass

def test_get_users_chats_invalid_id():
    pass