import json
from datetime import datetime
from uuid import uuid4
from backend.entities import (
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    MessageInDB,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

def get_all_users() -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    return [UserInDB(**user_data) for user_data in DB["users"].values()]

def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """

    user = UserInDB(
        created_at=datetime.today(),
        **user_create.model_dump(),
    )
    DB["users"][user.id] = user.model_dump()
    return user

def get_user_by_id(user_id: str) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    pass

def get_users_chats(user_id: str) -> list[ChatInDB]:
    """
    Retrieve a users chats from the database.

    :param user_id: id of the user
    :return: ordered list of chats
    """
    pass

def get_all_chats() -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """
    return [ChatInDB(**chat_data) for chat_data in DB["chats"].values()]

def get_chat_by_id(chat_id: str) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    pass

def update_chat(chat_id: str, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update a chat in the database

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the animal
    :return: the updated chat
    """
    pass

def delete_chat(chat_id: str):
    """
    Delete a chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """
    pass

def get_chat_messages(chat_id: str) -> list[MessageInDB]:
    """
    Retrieve a chats messages from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat messages
    """
    pass

def get_chat_users(chat_id: str) -> list[UserInDB]:
    """
    Retrieve a chats users from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat users
    """
    pass