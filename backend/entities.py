from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)

class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""
    id: int

class UserUpdate(BaseModel):
    """Request model for updating user in the system."""
    username: str = None
    email: str = None

class User(SQLModel):
    """Represents a user."""
    id: int
    username: str
    email: str
    created_at: datetime

class UserResponse(BaseModel):
    """Represents a response for a user."""
    user: User

class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")

class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")

class ChatUpdate(BaseModel):
    """Represents parameters for updating a chat in the system."""
    name: str = None

class Chat(SQLModel):
    """Represents a chat."""
    id: int
    name: str
    owner: User
    created_at: datetime

class Message(SQLModel):
    """Represents a message."""
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime

class MessageResponse(BaseModel):
    """Represents a response for a message."""
    message: Message

class ChatMetadata(BaseModel):
    """Represents metadata for a chat."""
    message_count: int
    user_count: int

class ChatResponse(BaseModel):
    """Represents a response for a chat."""
    chat: Chat

class ChatResponseWithMeta(BaseModel):
    """Represents a response for a chat."""
    meta: ChatMetadata
    chat: Chat
    messages: list[Message] = None
    users: list[User] = None

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    users: list[User]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    meta: Metadata
    chats: list[Chat]

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""
    meta: Metadata
    messages: list[Message]