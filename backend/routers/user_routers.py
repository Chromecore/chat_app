from fastapi import APIRouter
from backend import database as db
from backend.entities import (
    UserCollection, 
    ChatCollection,
    UserInDB,
    UserCreate,
    UserResponse,
)

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", response_model=UserCollection)
def get_users():
    """Get all users sorted by ID."""
    users = db.get_all_users()

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=lambda user: user.id),
    )

@users_router.post("", response_model=UserResponse)
def create_user(user_create: UserCreate):
    """Adds a new user."""
    return UserResponse(user=db.create_user(user_create))

@users_router.get("/{user_id}", response_model=UserResponse,
                  description="Get a user for a given user id.")
def get_user(user_id: str):
    """Get a user by id."""
    return UserResponse(user=db.get_user_by_id(user_id))

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_users_chats(user_id: str):
    """Gets all chats from a user by user id."""
    chats = db.get_users_chats(user_id)

    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: chat.name),
    )