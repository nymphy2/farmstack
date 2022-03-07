from bson.objectid import ObjectId
from typing import Optional

from pydantic import BaseModel, Field

from models.objectid import PyObjectId
from schemas.token import Token


class UserBase(BaseModel):
    email: str
    password: str

    class Config:
        allow_population_by_field_name: True
        arbitrary_types_allowed: True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'email': 'email@example.com',
                'password': 'password'
            }
        }


class UserModel(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str


class UserResponse(BaseModel):
    token: Token
    result: UserModel


class UserSignUp(UserBase):
    confirmPassword: str
    firstName: str
    lastName: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'email@example.com',
                'password': 'password',
                'confirmPassword': 'password',
                'firstName': 'Jon',
                'lastName': 'Wick'
            }
        }


class UserSignIn(UserBase):
    confirmPassword: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'email': 'email@example.com',
                'password': 'password',
            }
        }
