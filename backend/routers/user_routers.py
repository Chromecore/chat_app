from fastapi import APIRouter, Depends
from backend import database as db
from sqlmodel import Session
from backend.entities import (
    UserCollection, 
    ChatCollection,
    UserCreate,
    UserResponse,
    UserInDB,
    UserUpdate,
)
from backend.auth import get_current_user

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", response_model=UserCollection)
def get_users(session: Session = Depends(db.get_session)):
    """Get all users sorted by ID."""
    users = db.get_all_users(session)

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=lambda user: user.id),
    )


@users_router.get("/{user_id}", response_model=UserResponse,
                  description="Get a user for a given user id.",)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    """Get a user by id."""
    return UserResponse(user=db.get_user_by_id(session, user_id))


@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_users_chats(user_id: int, session: Session = Depends(db.get_session)):
    """Gets all chats from a user by user id."""
    chats = db.get_users_chats(session, user_id)

    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: chat.name),
    )


@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=user)


@users_router.put("/me", response_model=UserResponse)
def update_user(user_update: UserUpdate, 
                user: UserInDB = Depends(get_current_user),
                session: Session = Depends(db.get_session)
                ):
    """Update current user."""
    return UserResponse(user=db.update_user(session, user.id, user_update))