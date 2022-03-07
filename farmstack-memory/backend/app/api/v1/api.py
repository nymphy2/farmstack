from fastapi import APIRouter

from api.v1.endpoints import posts, user

api_router = APIRouter()
api_router.include_router(posts.router, prefix='/posts', tags=['posts'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
