import os
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, SQLModel, select

from backend import database as db
from backend.entities import UserResponse, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_key = os.environ.get("JWT_KEY")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str

class AuthException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=401,
            detail={
                "error": error,
                "error_description": description,
            },
        )

@auth_router.post("/registration", response_model=UserResponse)
def register_new_user(
    registration: UserRegistration,
    # session: Session = Depends(db.get_session),
    session: Annotated[Session, Depends(db.get_session)],
):
    """Register new user."""

    hashed_password = pwd_context.hash(registration.password)
    user = UserInDB(
        **registration.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user