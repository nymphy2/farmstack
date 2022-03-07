import math
from bson.objectid import ObjectId

from fastapi.encoders import jsonable_encoder

from db.database import db
from schemas.post import PostModel, PostCreate, PostPage, PostSearch


async def find_post_by_id(id: str) -> PostModel:
    object_id = ObjectId(id)
    doc = await db['postmessages'].find_one({'_id': object_id})
    return doc


async def find_posts_by_page(page: int) -> PostPage:
    '''Query posts by page.'''
    LIMIT: int = 8
    docs = []
    total = await db['postmessages'].count_documents({})
    start_index = (page - 1) * LIMIT
    cursor = db['postmessages'].find()
    cursor.sort('_id', -1).skip(start_index).limit(LIMIT)
    async for doc in cursor:
        docs.append(doc)
    return {'data': docs, 'currentPage': page, 'numberOfPages': math.ceil(total / LIMIT)}


async def find_posts_by_search(title: str, tags: str) -> PostSearch:
    """Query post by title and tags

    Args:
        title (str): posts' title
        tags (str): a string divide by comma. str,str

    Returns:
        PostSearch: list of queried post.
    """
    docs = []
    tag_list = tags.split(',') if tags is not None else []
    cursor = db['postmessages'].find(
        {'$or': [{'title': {'$regex': title, '$options': 'i'}}, {'tags': {'$in': tag_list}}]})
    async for doc in cursor:
        docs.append(doc)
    return {'data': docs}


async def insert_post(post: PostCreate) -> PostModel:
    doc_in = jsonable_encoder(post)
    new_doc = await db['postmessages'].insert_one(doc_in)
    created_doc = await db['postmessages'].find_one({'_id': new_doc.inserted_id})
    return created_doc


async def update_post_by_id(id: str, update_field) -> PostModel:
    object_id = ObjectId(id)
    doc_update = jsonable_encoder(update_field)
    result = await db['postmessages'].update_one({'_id': object_id}, {'$set': doc_update})
    new_doc = await find_post_by_id(id)
    return new_doc


async def delete_post_by_id(id: str):
    object_id = ObjectId(id)
    result = await db['postmessages'].delete_one({'_id': object_id})
    return result
