from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/comments", tags=["comments"])


class Comment(BaseModel):
    comment_text: str


"""
@router.get("/id/{comment_id}/", description="Get a comment for its ID")
def read_comment_from_id(comment_id: int):
    return 63
"""


@router.get("/id/icihihi/", description="Get a comment for its ID")
def read_comment_from_id(comment: Comment):
    print(comment.comment_text)
    return 63


@router.get("/frompost/", description="Get all comments from a post")
def read_comments_from_post(post_id: int):
    return -1


@router.put("/new/")
def create_comment(comment_id: int, text: str):
    return {"status": "success"}


@router.put("/delete/")
def delete_comment(comment_id: int):
    raise NotImplementedError()
