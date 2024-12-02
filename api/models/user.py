from pydantic import BaseModel
from typing import Optional, List
from api.models.movies import Movie


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    age: int
    sex: str
    email: str
    favourite_movies: List[Movie]


class UserMongo(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    age: int
    sex: str
    email: str
    favourite_movies: List[str]


class UserAPI(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    age: int
    sex: str
    email: str
    favourite_movies: List[Movie]
