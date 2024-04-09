from typing import Optional
from fastapi import APIRouter, Depends, Query
from backend import database as db
from sqlmodel import Session
from backend.entities import (
    ChatCollection,
    ChatUpdate,
    MessageCollection,
    ChatResponse,
    UserCollection,
    MessageResponse,
    UserInDB,
    ChatResponseWithMeta,
    ChatMetadata,
    MessageCreate,
    MessageUpdate,
)
from backend.auth import get_current_user

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("", response_model=ChatCollection)
def get_chats(user: UserInDB = Depends(get_current_user),
              session: Session = Depends(db.get_session)):
    """Get all chats sorted by name."""
    chats = db.get_all_chats(session, user)

    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: chat.name),
    )


@chats_router.get("/{chat_id}", response_model=ChatResponseWithMeta,
                  description="Get a chat for a given chat id.",
                  response_model_exclude_none=True)
def get_chat(chat_id: str,
             include: list[str] = Query(None),
             user: UserInDB = Depends(get_current_user),
             session: Session = Depends(db.get_session),
             ):
    """Get a chat by id."""
    chat = db.get_chat_by_id(session, chat_id)

    # get messages and users
    messages = None
    users = None
    if(include is not None and "messages" in include):
        messages = chat.messages
    if(include is not None and "users" in include):
        users = chat.users

    return ChatResponseWithMeta(
        meta=ChatMetadata(
            message_count = len(chat.messages),
            user_count = len(chat.users),
        ),
        chat = chat,
        messages = messages,
        users = users,
    )


@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """Updates a chat by id."""
    return ChatResponse(chat=db.update_chat(session, chat_id, chat_update))


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(chat_id: str,
                      #user: UserInDB = Depends(get_current_user),
                      session: Session = Depends(db.get_session)):
    """Gets a chats messages by chat id."""
    messages = db.get_chat_messages(session, chat_id)

    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=lambda message: message.created_at),
    )


@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_chat_users(chat_id: str, 
                   user: UserInDB = Depends(get_current_user),
                   session: Session = Depends(db.get_session)):
    """Gets a chats users by chat id."""
    users = db.get_chat_users(session, chat_id)

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=lambda user: user.id),
    )

@chats_router.post("/{chat_id}/messages", status_code=201, response_model=MessageResponse)
def create_new_message(chat_id: int,
                       text: MessageCreate,
                       user: UserInDB = Depends(get_current_user),
                       session: Session = Depends(db.get_session)
                       ):
    """Create a new message for the current user."""
    message = db.create_message(session, chat_id, user.id, text.text)
    return MessageResponse(message=message)


@chats_router.put("/{chat_id}/messages/{message_id}", response_model=MessageResponse)
def update_message(chat_id: int, message_id: int,
                 message: MessageUpdate,
                 user: UserInDB = Depends(get_current_user),
                 session: Session = Depends(db.get_session)):
    """Updates a message in a certain chat"""
    message = db.update_message(session, chat_id, message_id, message, user.id)
    return MessageResponse(message=message)

@chats_router.delete("/{chat_id}/messages/{message_id}", status_code=204)
def delete_message(chat_id: int, message_id: int,
                user: UserInDB = Depends(get_current_user),
                session: Session = Depends(db.get_session)):
    """Deletes a message in a certain chat"""
    db.delete_message(session, chat_id, message_id, user.id)