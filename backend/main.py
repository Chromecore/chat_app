from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from backend.routers.user_routers import users_router
from backend.routers.chat_routers import chats_router
from backend.database import EntityNotFoundException

# python -m uvicorn backend.main:app --reload

app = FastAPI(
    title="Pony Express API",
    description="API for managing users and chats",
    version="0.0.1",
)

app.include_router(users_router)
app.include_router(chats_router)

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

# can run as an application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", reload=True)