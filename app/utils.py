from datetime import datetime
from typing import List, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field, validator

server_path = "mongodb://localhost:27017/"


def date_format(date_string):
    if date_string is not None:
        try:
            res = datetime.strptime(date_string, "%Y-%m-%d")
        except Exception:
            raise ValueError("Date has a wrong format, use YYYY-MM-DD")


class User(BaseModel):
    username: str
    signature: Optional[str] = None
    # save as str as pymong does not support datetime.date, and FastAPI doe does not convert YYYY-MM-DD
    birthdate: Optional[str] = None
    posts: Optional[List[str]] = []

    @validator("birthdate")
    def birthdate_check(cls, v):
        date_format(v)
        return v


class PostContent(BaseModel):
    title: str
    text: str
    category: str
    _date: Optional[datetime] = None


class UserEdit(BaseModel):
    username: str
    signature: Optional[str]
    birthdate: Optional[str]

    @validator("birthdate")
    def birthdate_check(cls, v):
        date_format(v)
        return v


class PostEdit(BaseModel):
    title: Optional[str]
    text: Optional[str]
    category: Optional[str]
