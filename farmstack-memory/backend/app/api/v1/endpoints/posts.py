from typing import Optional

from fastapi import APIRouter, HTTPException, status, Body, Query, Depends
from fastapi.responses import ORJSONResponse

from schemas.post import PostModel, PostCreate, PostUpdate, PostPage, PostSearch, PostCommnet, PostLike
from api.deps import get_current_user_id
from crud.curd_post import (
    find_post_by_id,
    find_posts_by_page,
    find_posts_by_search,
    insert_post,
    update_post_by_id,
    delete_post_by_id
)

router = APIRouter()


@router.get(
    '/',
    response_description='get post for page',
    response_model=PostPage,
    response_class=ORJSONResponse
)
async def get_posts(page: int = Query(1)):
    if(posts := await find_posts_by_page(page)) is not None:
        return posts

    raise HTTPException(status_code=404, detail='Posts not found')


@router.get(
    '/search',
    response_description='Get post by title and tags',
    response_model=PostSearch,
    response_class=ORJSONResponse,
)
async def get_posts_by_search(
    title: str = Query('none'),
    tags: Optional[str] = Query(None)
):
    if(posts := await find_posts_by_search(title, tags)) is not None:
        return posts

    raise HTTPException(status_code=404,
                        detail=f'post with title: {title} or tags: {tags} not exist')


@router.get('/{id}', response_model=PostModel)
async def get_post(id: str):
    if(post := await find_post_by_id(id)) is not None:
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} is not exist')


@router.post(
    '/',
    response_description='Added post',
    response_model=PostModel,
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: PostCreate = Body(...),
    user_id=Depends((get_current_user_id))
):
    new_post = post.dict()
    new_post['creator'] = user_id
    created_post = await insert_post(new_post)
    return created_post


@router.post(
    '/{id}/commentPost',
    response_model=PostModel,
    response_class=ORJSONResponse,
    dependencies=[Depends(get_current_user_id)]
)
async def comment_post(id: str, comment_value: str = Body(...)):
    post = await find_post_by_id(id)
    post.get('comments').append(comment_value)
    updated_obj = PostCommnet(**post)
    updated_post = await update_post_by_id(id, updated_obj)
    return updated_post


@router.patch(
    '/{id}',
    response_description='Updated post',
    response_model=PostModel,
    response_class=ORJSONResponse,
    dependencies=[Depends(get_current_user_id)]
)
async def update_post(id: str, post: PostUpdate = Body(...)):
    updated_post = await update_post_by_id(id, post)
    return updated_post


@router.patch(
    '/{id}/likePost',
    response_model=PostModel,
    response_class=ORJSONResponse
)
async def like_post(id: str, user_id: str = Depends(get_current_user_id)):
    if(
        post := await find_post_by_id(id)
    ) is not None:
        likes = post.get('likes')
        if (likes.count(user_id) == 1):
            likes.remove(user_id)
        else:
            likes.append(user_id)
        update_obj = PostLike(**post)
        updated_post = await update_post_by_id(id, update_obj)
        return updated_post

    raise HTTPException(status_code=404, detail=f'No post with id: {id}')


@router.delete(
    '/{id}',
    dependencies=[Depends(get_current_user_id)]
)
async def delete_post(id: str) -> str:
    if find_post_by_id(id) is not None:
        delete_result = await delete_post_by_id(id)
        if(delete_result.deleted_count == 1):
            return ORJSONResponse({'message': 'Post delete successful'})

        raise HTTPException(
            status_code=404, detail=f'Post with id {id} does not exist')
