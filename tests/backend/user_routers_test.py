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
    create_params = {
        "id": "My Cool ID",
    }
    client = TestClient(app)
    response = client.post("/users", json=create_params)
    assert response.status_code == 200

    user = response.json()
    for key, value in create_params.items():
        assert user["user"][key] == value

    response = client.get(f"/users/{user['user']['id']}")
    assert response.status_code == 200

    user = response.json()
    for key, value in create_params.items():
        assert user["user"][key] == value

def test_create_user_duplicate():
    user_id = "bishop"
    create_params = {
        "id": user_id,
    }
    client = TestClient(app)
    response = client.post("/users", json=create_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }

def test_get_user_by_id():
    user_id = "bishop"
    expected_response = {
        "user": {
            "id": user_id,
            "created_at": "2014-04-14T10:49:07",
        }
    }
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user_invalid_id():
    user_id = "invalid_id"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }

def test_get_users_chats():
    user_id = "bishop"
    expected_response = {
        "meta": {
            "count": 1
        },
        "chats": [
            {
            "id": "734eeb9ddaec43b2ab6e289a0d472376",
            "name": "nostromo",
            "user_ids": [
                "bishop",
                "burke",
                "ripley"
            ],
            "owner_id": "ripley",
            "created_at": "2023-09-18T14:18:46"
            }
        ]
    }
    client = TestClient(app)
    response = client.get(f"/users/{user_id}/chats")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_users_chats_invalid_id():
    user_id = "invalid_id"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}/chats")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }