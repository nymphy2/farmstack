from bson import ObjectId
from datetime import datetime
from typing import List

from pydantic import BaseModel


class PostMessage(BaseModel):
    _id: ObjectId
    title: str
    message: str
    name: str
    creator: str
    tags: List[str]
    likes: List[str] = []
    comments: List[str] = []
    createdAt: datetime = datetime.now()
    selectedFile: str