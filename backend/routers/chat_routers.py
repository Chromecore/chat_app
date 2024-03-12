from fastapi import APIRouter, Depends
from backend import database as db
from sqlmodel import Session
from backend.entities import (
    ChatCollection,
    ChatUpdate,
    MessageCollection,
    ChatResponse,
    UserCollection,
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("", response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    """Get all chats sorted by name."""
    chats = db.get_all_chats(session)

    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: chat.name),
    )


@chats_router.get("/{chat_id}", response_model=ChatResponse,
                  description="Get a chat for a given chat id.")
def get_chat(chat_id: str, session: Session = Depends(db.get_session)):
    """Get a chat by id."""
    return ChatResponse(chat=db.get_chat_by_id(session, chat_id))


@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """Updates a chat by id."""
    return ChatResponse(chat=db.update_chat(session, chat_id, chat_update))


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(chat_id: str, session: Session = Depends(db.get_session)):
    """Gets a chats messages by chat id."""
    messages = db.get_chat_messages(session, chat_id)

    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=lambda message: message.created_at),
    )


@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_chat_users(chat_id: str, session: Session = Depends(db.get_session)):
    """Gets a chats users by chat id."""
    users = db.get_chat_users(session, chat_id)

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=lambda user: user.id),
    )