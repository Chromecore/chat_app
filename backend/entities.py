from datetime import datetime
from pydantic import BaseModel, Field

class UserInDB(BaseModel):
    """Represents a User in the database."""
    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""
    id: str

class ChatInDB(BaseModel):
    """Represents a chat in the database."""
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class ChatUpdate(BaseModel):
    """Represents parameters for updating a chat in the system."""
    name: str = None

class MessageInDB(BaseModel):
    """Represents a Message in the database."""
    id: str
    user_id: str
    text: str
    created_at: datetime

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    users: list[UserInDB]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    meta: Metadata
    chats: list[ChatInDB]

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""
    meta: Metadata
    messages: list[MessageInDB]