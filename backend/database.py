import json
from datetime import datetime
from uuid import uuid4
from backend.entities import (
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    MessageInDB,
    ChatWithMessagesInDB,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
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

    if(user_create.id in DB["users"]):
        raise DuplicateEntityException(entity_name="User", entity_id=user_create.id)

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
    if(user_id in DB["users"]):
        return UserInDB(**DB["users"][user_id])
    
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def get_users_chats(user_id: str) -> list[ChatInDB]:
    """
    Retrieve a users chats from the database.

    :param user_id: id of the user
    :return: ordered list of chats
    """
    if(user_id not in DB["users"]):
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)

    chats = get_all_chats()
    return [chat for chat in chats if chat.user_ids.__contains__(user_id)]

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
    if(chat_id in DB["chats"]):
        return ChatInDB(**DB["chats"][chat_id])
    
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_chat_with_messages_by_id(chat_id: str) -> ChatWithMessagesInDB:
    """
    Retrieve a chat with its messages from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    if(chat_id in DB["chats"]):
        return ChatWithMessagesInDB(**DB["chats"][chat_id])
    
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(chat_id: str, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update a chat in the database

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the animal
    :return: the updated chat
    """
    chat = get_chat_by_id(chat_id)

    for attr, value, in chat_update.model_dump(exclude_none=True).items():
        setattr(chat, attr, value)
    
    DB["chats"][chat.id] = chat.model_dump()

    return chat

def delete_chat(chat_id: str):
    """
    Delete a chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """
    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]

def get_chat_messages(chat_id: str) -> list[MessageInDB]:
    """
    Retrieve a chats messages from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat messages
    """
    return [message_data for message_data in get_chat_with_messages_by_id(chat_id).messages]

def get_chat_users(chat_id: str) -> list[UserInDB]:
    """
    Retrieve a chats users from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat users
    """
    chat = get_chat_by_id(chat_id)
    all_users = get_all_users()
    return [user for user in all_users if chat.user_ids.__contains__(user.id)]