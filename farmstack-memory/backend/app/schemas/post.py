from datetime import datetime
from typing import List, Optional
from bson.objectid import ObjectId

from pydantic import BaseModel, Field

from models.objectid import PyObjectId


class PostBase(BaseModel):
    class Config:
        allow_population_by_field_name: True
        arbitrary_types_allowed: True
        json_encoders = {ObjectId: str}


class PostModel(PostBase):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    title: str
    message: str
    name: str
    creator: str
    tags: List[str]
    likes: List[str] = []
    comments: List[str] = []
    createdAt: datetime = datetime.now()
    selectedFile: str


class PostCreate(PostBase):
    title: str
    message: str
    name: str
    creator: str = None
    tags: List[str]
    likes: List[str] = []
    comments: List[str] = []
    createdAt: datetime = datetime.now()
    selectedFile: str

    class Config:
        schema_extra = {
            'example': {
                'title': 'Eiffel Tower',
                'message': 'some messages',
                'name': 'Jon Wick',
                'tags': ['2022', 'tower'],
                'selectedFile': 'some file'
            }
        }


class PostPage(PostBase):
    data: List[PostModel]
    currentPage: int
    numberOfPages: int


class PostSearch(PostBase):
    data: Optional[List[PostModel]]


class PostUpdate(PostBase):
    title: Optional[str]
    message: Optional[str]
    tags: Optional[List[str]]
    selectedFile: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'title': 'Eiffel Tower',
                'message': 'some messages',
                'tags': ['2022', 'tower'],
                'selectedFile': 'some file'
            }
        }


class PostCommnet(PostBase):
    comments: Optional[List[str]] = None


class PostLike(PostBase):
    likes: Optional[List[str]] = None
