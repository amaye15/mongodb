from pydantic import BaseModel


class Database(BaseModel):
    name: str
