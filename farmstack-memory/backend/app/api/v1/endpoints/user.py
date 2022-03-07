from datetime import timedelta

from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import ORJSONResponse

from schemas.user import UserResponse, UserSignUp, UserSignIn
from core.security import create_access_token
from crud.crud_user import (
    find_user_by_email,
    authenticate_user,
    insert_user,
)

router = APIRouter()


@router.post('/signin')
async def signin(user: UserSignIn = Body(...)) -> UserResponse:
    user_obj = await authenticate_user(user.email, user.password)
    user_id = dict(user_obj).get('_id')
    token_expire_in = timedelta(minutes=60)
    return ORJSONResponse({
        'token': create_access_token(user_id, expires_delta=token_expire_in),
        'result': user_obj
    })


@router.post('/signup')
async def signup(user: UserSignUp = Body(...)) -> UserResponse:
    user_obj = await find_user_by_email(user.email)
    if user_obj:
        raise HTTPException(status_code=400, detail='User already exist')
    if(user.password != user.confirmPassword):
        raise HTTPException(status_code=400, detail='Password do not match')
    user_obj = await insert_user(user)
    user_id = dict(user_obj).get('_id')
    token_expires_in = timedelta(minutes=60)
    return ORJSONResponse({
        'token': create_access_token(user_id, expires_delta=token_expires_in),
        'result': user_obj
    })
