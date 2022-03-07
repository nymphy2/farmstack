from typing import Optional
from bson.objectid import ObjectId

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


from db.database import db
from schemas.user import UserModel, UserSignUp
from core.security import hashing_password, verify_password


async def find_user_by_id(id: str) -> Optional[UserModel]:
    doc = await db['users'].find_one({'_id': id})
    return doc


async def find_user_by_email(email: str) -> Optional[UserModel]:
    doc = await db['users'].find_one({'email': email})
    return doc


async def insert_user(user: UserSignUp) -> UserModel:
    doc_in = UserModel(
        email=user.email,
        password=hashing_password(user.password),
        # name should be combination of first name and last name
        name=' '.join([user.firstName, user.lastName])
    )
    new_doc = await db['users'].insert_one(jsonable_encoder(doc_in))
    created_doc = await db['users'].find_one({'_id': new_doc.inserted_id})
    return created_doc


async def authenticate_user(email: str, password: str) -> Optional[UserModel]:
    existing_user = await find_user_by_email(email)
    if not existing_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    if not verify_password(password, existing_user.get('password')):
        raise HTTPException(status_code=400, detail='Incorrect password')
    return existing_user
