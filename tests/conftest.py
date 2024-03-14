import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine
from datetime import datetime
from backend.main import app
from backend import database as db
from backend import auth

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def logged_in_client(session, user_fixture):
    def _get_session_override():
        return session

    def _get_current_user_override():
        return user_fixture(username="juniper")

    app.dependency_overrides[db.get_session] = _get_session_override
    app.dependency_overrides[auth.get_current_user] = _get_current_user_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def user_fixture(session):
    def _build_user(
        username: str = "name",
        email: str = "@cool.email",
        password: str = "password",
    ) -> db.UserInDB:
        return auth.register_new_user(
            auth.UserRegistration(
                username=username,
                email=email,
                password=password,
            ),
            session,
        )

    return _build_user

@pytest.fixture
def chat_fixture(session):
    def _build_chat(
        name: str = "chat007",
        owner_id: int = 0,
    ) -> db.ChatInDB:
        chat = db.ChatInDB(
            name=name,
            owner_id=owner_id,
        )

        session.add(chat)
        session.commit()
        session.refresh(chat)

        return chat

    return _build_chat