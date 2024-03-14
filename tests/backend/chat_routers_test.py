from fastapi.testclient import TestClient
from backend.main import app
import pytest
from backend.entities import ChatInDB, UserChatLinkInDB, MessageInDB

@pytest.fixture
def default_chats():
    return [
        ChatInDB(
            name="chat1",
            owner_id=1,
        ),
        ChatInDB(
            name="chat2",
            owner_id=1,
        ),
        ChatInDB(
            name="chat3",
            owner_id=2,
        ),
    ]

def test_get_all_chats(client, chat_fixture, user_fixture):
    user = user_fixture(username="bishop", email="testemail").user
    db_chats = [
        chat_fixture(name=name, owner_id=user.id)
        for name in ["test", "chat", "hi"]
    ]
    expected_chats = ["test", "chat", "hi"]

    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]

    assert meta["count"] == len(chats)
    assert [chat.name for chat in db_chats] == expected_chats

def test_get_chat_by_id(client, chat_fixture, user_fixture, session):
    user = user_fixture(username="bishop", email="testemail").user
    chat = chat_fixture(name="chatName", owner_id=user.id)
    link = UserChatLinkInDB(user_id=user.id, chat_id=chat.id)
    session.add(link)
    session.commit()
    session.refresh(link)

    chat_id = 1
    expected_response = {
        "meta": {
            "message_count": 0,
            "user_count": 1
        },
        "chat": {
            "id": chat.id,
            "name": "chatName",
            "owner": {
                "id": user.id,
                "username": "bishop",
                "email": "testemail",
                "created_at": user.created_at.isoformat()
            },
            "created_at": chat.created_at.isoformat()
            }
    }
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_chat_invalid_id(client):
    chat_id = 67
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": str(chat_id),
        },
    }

def test_update_chat(client, chat_fixture, user_fixture):
    user = user_fixture(username="bishop", email="testemail").user
    chat = chat_fixture(name="chatName", owner_id=user.id)

    update_params = {"name": "New Chat Name"}
    expected_response = {
        "chat": {
            "id": chat.id,
            "name": update_params["name"],
            "owner": {
                "id": user.id,
                "username": "bishop",
                "email": "testemail",
                "created_at": user.created_at.isoformat()
            },
            "created_at": chat.created_at.isoformat()
            }
    }
    response = client.put(f"/chats/{chat.id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == expected_response

    expected_response = {
        "meta": {
            "message_count": 0,
            "user_count": 0
        },
        "chat": {
            "id": chat.id,
            "name": update_params["name"],
            "owner": {
                "id": user.id,
                "username": "bishop",
                "email": "testemail",
                "created_at": user.created_at.isoformat()
            },
            "created_at": chat.created_at.isoformat()
            }
    }

    # test that the update is persisted
    response = client.get(f"/chats/{chat.id}")
    assert response.status_code == 200
    assert response.json() == expected_response

def test_update_chat_invalid_id(client):
    chat_id = 67
    update_params = {
        "name": "updated name",
    }
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": str(chat_id),
        },
    }

def test_get_chat_messages(client, session, chat_fixture, user_fixture):
    user = user_fixture(username="bishop", email="testemail").user
    chat = chat_fixture(name="chatName", owner_id=user.id)
    message = MessageInDB(text="New Message", user_id=user.id, chat_id=chat.id)
    session.add(message)
    session.commit()
    session.refresh(message)

    response = client.get(f"/chats/{chat.id}/messages")
    assert response.status_code == 200
    assert response.json() == {
        "meta": {
            "count": 1
        },
        "messages": [
            {
            "id": message.id,
            "text": "New Message",
            "chat_id": chat.id,
            "user": {
                "id": user.id,
                "username": "bishop",
                "email": "testemail",
                "created_at": user.created_at.isoformat()
            },
            "created_at": message.created_at.isoformat()
            },
        ]
    }

def test_get_chat_messages_invalid_id(client):
    chat_id = 78
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": str(chat_id),
        },
    }

def test_get_chat_users_invalid_id(client):
    chat_id = 78
    response = client.get(f"/chats/{chat_id}/users")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": str(chat_id),
        },
    }