from fastapi import APIRouter
from backend import database as db
from backend.entities import (
    UserCollection, 
    ChatCollection,
    UserInDB,
    UserCreate
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

@users_router.post("", response_model=UserInDB)
def create_user(user_create: UserCreate):
    """Adds a new user."""
    return db.create_user(user_create)

@users_router.get("/{user_id}", response_model=UserInDB)
def get_user_by_id(user_id: str):
    """Get a user by id."""
    pass

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_users_chats():
    """Gets all chats from a user by user id."""
    pass