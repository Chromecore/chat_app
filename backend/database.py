from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, select
from backend.entities import (
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    MessageInDB,
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
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


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

def get_user_by_id(session: Session, user_id: str) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user
    
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def get_users_chats(session: Session, user_id: str) -> list[ChatInDB]:
    """
    Retrieve a users chats from the database.

    :param user_id: id of the user
    :return: ordered list of chats
    """
    get_user_by_id(session, user_id)
    chats = get_all_chats(session)
    return [chat for chat in chats if user_id in chat.user_ids]


#   -------- Chats --------   #


def get_all_chats(session: Session) -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """
    return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, chat_id: str) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """

    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

# def get_chat_with_messages_by_id(session: Session, chat_id: str) -> ChatWithMessagesInDB:
#     """
#     Retrieve a chat with its messages from the database.

#     :param chat_id: id of the chat to be retrieved
#     :return: the retrieved chat
#     """
#     if(chat_id in DB["chats"]):
#         return ChatWithMessagesInDB(**DB["chats"][chat_id])
    
#     raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: str, chat_update: ChatUpdate) -> ChatInDB:
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

def delete_chat(session: Session, chat_id: str):
    """
    Delete a chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """
    chat = get_chat_by_id(session, chat_id)
    session.delete(chat)
    session.commit()

def get_chat_messages(session: Session, chat_id: str) -> list[MessageInDB]:
    """
    Retrieve a chats messages from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat messages
    """

    chat = get_chat_by_id(session, chat_id)

    return chat.messages

def get_chat_users(session: Session, chat_id: str) -> list[UserInDB]:
    """
    Retrieve a chats users from the database.

    :param chat_id: id of the chat
    :return: ordered list of chat users
    """
    chat = get_chat_by_id(session, chat_id)
    all_users = get_all_users(session)
    return [user for user in all_users if chat.user_ids.__contains__(user.id)]