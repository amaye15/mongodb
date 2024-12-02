from typing import List
from fastapi import APIRouter
from api.models.user import User
from api.database.queries import add_document

router = APIRouter()


users = []


# Endpoint to create a new user
@router.post("/create_user", response_model=User)
async def create_user(user: User):
    # users.append(user)
    result = await add_document(user.model_dump(), collection_name="user")
    print(result, flush=True)
    return user


# Endpoint to get all users
@router.get("/get_user", response_model=List[User])
async def get_users():
    return users
