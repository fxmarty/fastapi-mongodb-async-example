import re
from datetime import datetime
from enum import Enum
from typing import List, Optional

import pydantic
import pymongo
from bson import ObjectId, json_util
from fastapi import APIRouter, Body, Path, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..utils import PostContent, PostEdit, User, date_format, server_path

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = pymongo.MongoClient(server_path)

project_db = client.project
users_collection = project_db.get_collection("users")
posts_collection = project_db.get_collection("posts")

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/search", description="Search for a post")
def search_posts(
    title: Optional[str] = Query(
        None, description="Text to find in the title of the post"
    ),
    text: Optional[str] = Query(
        None, description="Text to find in the body of the post"
    ),
    post_id: Optional[str] = Query(None, description="Post id"),
    author: Optional[str] = Query(None, description="Filter by author"),
    start: Optional[str] = Query(None, description="Starting time"),
    end: Optional[str] = Query(None, description="Ending time"),
):
    query_dict = {"_date": {}}
    if start:
        print("start is not None")
        date_format(start)
        start_datetime = datetime.strptime(start, "%Y-%m-%d")
        query_dict["_date"]["$gte"] = start_datetime
    if end:
        date_format(end)
        end_datetime = datetime.strptime(start, "%Y-%m-%d")
        query_dict["_date"]["$lte"] = end_datetime
    if author:
        query_dict["author"] = author
    if title:
        query_dict["title"] = re.compile(f"^.*{title}.*$", re.IGNORECASE)
    if text:
        query_dict["text"] = re.compile(f"^.*{title}.*$", re.IGNORECASE)
    if post_id:
        try:
            query_dict["_id"] = ObjectId(post_id)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    if len(query_dict["_date"]) == 0:
        del query_dict["_date"]

    cursor = posts_collection.find(query_dict)

    res = json_util.dumps(cursor)

    return JSONResponse(status_code=status.HTTP_200_OK, content=res)


@router.put("/new")
def create_post(username: str, post_content: PostContent):
    if users_collection.count_documents({"username": username}) == 0:
        user_json = jsonable_encoder(User(username=username))
        result = users_collection.insert_one(user_json)

    post_json = jsonable_encoder(post_content)
    post_json["_date"] = datetime.now()
    post_json["author"] = username
    result = posts_collection.insert_one(post_json)
    print(result)

    result = users_collection.update_one(
        {"username": username}, {"$push": {"posts": post_json["_id"]}}
    )
    print(result)

    return post_json["_id"]


@router.put("/edit")
def edit_post(username: str, post_id: str, post: PostEdit):
    if users_collection.count_documents({"username": username}) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User do not exist"
        )
    elif posts_collection.count_documents({"_id": ObjectId(post_id)}) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="Post do not exist"
        )
    else:
        updates = post.dict(exclude_unset=True)
        updates["_date"] = datetime(2021, 2, 12)
        filter_row = {"_id": ObjectId(post_id)}
        result = posts_collection.update_one(filter_row, {"$set": updates})
        print(result)
        return "Updated post"


@router.put("/delete")
def delete_post(username: str, post_id: str):
    if users_collection.count_documents({"username": username}) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User do not exist"
        )
    elif posts_collection.count_documents({"_id": ObjectId(post_id)}) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="Post do not exist"
        )
    else:
        result = users_collection.update_one(
            {"username": username}, {"$pull": {"posts": ObjectId(post_id)}}
        )
        print(result)
        result = posts_collection.delete_one({"_id": ObjectId(post_id)})
        print(result)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=f"Removed post successfully"
        )
