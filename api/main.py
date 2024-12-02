from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.endpoints import users
from api.database import database_manager
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database_manager.try_connection()  # Properly await your async connection method
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(database_manager.router, prefix="/db", tags=["database"])


# try_connection()
@app.get("/", include_in_schema=False)  # Exclude from OpenAPI schema
async def redirect_to_docs():
    return RedirectResponse(url="/docs")  # Redirect to Swagger UI
