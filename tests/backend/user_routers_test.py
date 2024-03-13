from fastapi.testclient import TestClient
from backend.main import app
from backend.entities import UserChatLinkInDB

def test_get_all_users(client, user_fixture):
    db_users = [user_fixture(username=username, email=f'{username}@email.com') 
                for username in ["bob", "joe"]]
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]

    assert meta["count"] == len(db_users)
    assert {user["username"] for user in users} == {
        db_user.user.username for db_user in db_users
    }

def test_get_current_user_not_logged_in(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_get_user_by_id(client, user_fixture):
    user = user_fixture(username="bishop", email="testemail").user
    expected_response = {
        "user": {
            "id": user.id,
            "username": "bishop",
            "email": "testemail",
            "created_at": user.created_at.isoformat()
        }
    }
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user_invalid_id(client):
    response = client.get(f"/users/{67}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": 67,
        },
    }

def test_get_users_chats(client, session, user_fixture, chat_fixture):
    user = user_fixture(username="bishop", email="testemail").user
    chat = chat_fixture(name="NewChat", owner_id=user.id)
    link = UserChatLinkInDB(user_id=user.id, chat_id=chat.id)
    session.add(link)
    session.commit()
    session.refresh(link)

    expected_response = {
        "meta": {
            "count": 1
        },
        "chats": [
            {
            "id": chat.id,
            "name": "NewChat",
            "owner": {
                "id": user.id,
                "username": "bishop",
                "email": "testemail",
                "created_at": user.created_at.isoformat()
            },
            "created_at": chat.created_at.isoformat()
            }
        ]
    }
    response = client.get(f"/users/{user.id}/chats")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_users_chats_invalid_id(client):
    user_id = 69
    response = client.get(f"/users/{user_id}/chats")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id,
        },
    }