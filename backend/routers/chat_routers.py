from fastapi import APIRouter
from backend import database as db
from backend.entities import (
    ChatCollection,
    ChatInDB,
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("", response_model=ChatCollection)
def get_chats():
    """Get all chats sorted by name."""
    chats = db.get_all_chats()

    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: chat.name),
    )

@chats_router.get("/{chat_id}", response_model=ChatInDB)
def get_chat_by_id(chat_id: str):
    """Get a chat by id."""
    pass

@chats_router.put("/{chat_id}")
def update_chat(chat_id: str):
    """Updates a chat by id."""
    pass

@chats_router.delete("/{chat_id}")
def delete_chat(chat_id: str):
    """Deletes a chat by id."""
    pass

@chats_router.get("/{chat_id}/messages")
def get_chat_messages(chat_id: str):
    """Gets a chats messages by chat id."""
    pass

@chats_router.get("/{chat_id}/users")
def get_chat_users(chat_id: str):
    """Gets a chats users by chat id."""
    pass