from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, select
from fastapi import HTTPException
from backend.entities import (
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    MessageInDB,
    UserUpdate,
    MessageUpdate,
)

# create database engine
engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

#with open("backend/fake_db.json", "r") as f:
#    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id

class NoPermissionException(HTTPException):
    def __init__(self, action: str, entity: str):
        super().__init__(
            status_code=403,
            detail={
                "error": "no_permission",
                "error_description": f"requires permission to {action} {entity}"
            },
        )

#   -------- Users --------   #

def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    return session.exec(select(UserInDB)).all()

def create_user(session: Session, user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """
    user = session.get(UserInDB, user_create.id)
    if user:
        raise DuplicateEntityException(entity_name="User", entity_id=user_create.id)

    user = UserInDB(
        created_at=datetime.today(),
        **user_create.model_dump(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    """
    Update a user from the database.

    :param user_id: id of the user to be retrieved
    :param user_update: attributes to be updated
    :return: the updated user
    """
    user = get_user_by_id(session, user_id)
    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user
    
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def get_users_chats(session: Session, user_id: int) -> list[ChatInDB]:
    """
    Retrieve a users chats from the database.

    :param user_id: id of the user
    :return: ordered list of chats
    """
    user = get_user_by_id(session, user_id)
    chats = get_all_chats(session, user)
    return [chat for chat in chats if user in chat.users]


#   -------- Chats --------   #


def get_all_chats(session: Session, user: UserInDB) -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """
    # .where(user in ChatInDB.users)
    return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """

    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update a chat in the database

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the animal
    :return: the updated chat
    """
    chat = get_chat_by_id(session, chat_id)

    for attr, value, in chat_update.model_dump(exclude_none=True).items():
        setattr(chat, attr, value)
    
    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat

def delete_chat(session: Session, chat_id: int):
    """
    Delete a chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """
    chat = get_chat_by_id(session, chat_id)
    session.delete(chat)
    session.commit()

def get_chat_messages(session: Session, chat_id: int) -> list[MessageInDB]:
    """
    Retrieve a chats messages from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat messages
    """

    chat = get_chat_by_id(session, chat_id)

    return chat.messages

def get_chat_message_by_id(session: Session, chat_id: int, message_id: int) -> MessageInDB:
    """
    Retrieve a chats message by id from the database.

    :param chat_id: id of the chat
    :param message_id: id of the message
    :return: the chat message
    """
    messages = get_chat_messages(session, chat_id)
    for message in messages:
        if message.id == message_id:
            return message
    raise EntityNotFoundException(entity_name="Message", entity_id=message_id)

def update_message(session: Session, chat_id: int, 
                   message_id: int, message_update: MessageUpdate, 
                   user_id: int) -> MessageInDB:
    """
    Retrieve a chats message by id from the database.

    :param chat_id: id of the chat
    :param message_id: id of the message
    :param message_update: the new message
    :param user_id: the id of the current user
    :return: the updated message
    """
    message = get_chat_message_by_id(session, chat_id, message_id)
    if message.user.id != user_id:
        raise NoPermissionException(action="edit", entity="message")

    for attr, value, in message_update.model_dump(exclude_none=True).items():
        setattr(message, attr, value)
    
    session.add(message)
    session.commit()
    session.refresh(message)

    return message

def delete_message(session: Session, chat_id: int, 
                   message_id: int, user_id: int):
    """
    Delete a message by id from the database.

    :param chat_id: id of the chat
    :param message_id: id of the message
    :param user_id: the id of the current user
    """
    message = get_chat_message_by_id(session, chat_id, message_id)
    if message.user.id != user_id:
        raise NoPermissionException(action="delete", entity="message")
    session.delete(message)
    session.commit()


def get_chat_users(session: Session, chat_id: int) -> list[UserInDB]:
    """
    Retrieve a chats users from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat users
    """
    chat = get_chat_by_id(session, chat_id)
    all_users = get_all_users(session)
    return [user for user in all_users if chat.users.__contains__(user)]

def create_message(session: Session, chat_id: int, user_id: int, text: str) -> MessageInDB:
    """
    Adds a new message for the current user in the givin chat.

    :param chat_id: id of the chat
    :param user_id: id of the user
    :param text: the text for the message
    :return: the newly added message
    """
    get_chat_by_id(session, chat_id)

    message = MessageInDB(
        text = text,
        user_id = user_id,
        chat_id = chat_id,
    )

    session.add(message)
    session.commit()
    session.refresh(message)

    return message