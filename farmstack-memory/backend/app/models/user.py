from bson import ObjectId

from pydantic import BaseModel


class User(BaseModel):
    _id: ObjectId
    name: str
    email: str
    password: str