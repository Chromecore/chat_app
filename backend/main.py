from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from backend.routers.user_routers import users_router
from backend.routers.chat_routers import chats_router
from backend.database import EntityNotFoundException
from backend.database import DuplicateEntityException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import create_db_and_tables
from backend.auth import auth_router

# python -m uvicorn backend.main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express API",
    description="API for managing users and chats",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(users_router)
app.include_router(chats_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # change this as appropriate for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# handle custom exceptions
@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request, 
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "type": "entity_not_found",
                    "entity_name": exception.entity_name,
                    "entity_id": exception.entity_id
                }
            }
        )

@app.exception_handler(DuplicateEntityException)
def handle_duplicate_entity(
    _request: Request, 
    exception: DuplicateEntityException,
) -> JSONResponse:
    return JSONResponse(
            status_code=422,
            content={
                "detail": {
                    "type": "duplicate_entity",
                    "entity_name": exception.entity_name,
                    "entity_id": exception.entity_id
                }
            }
        )

# can run as an application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", reload=True)