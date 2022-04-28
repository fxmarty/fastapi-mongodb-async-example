from enum import Enum
from typing import List, Optional

import pydantic
from bson import ObjectId, json_util
from fastapi import APIRouter, Body, Path, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..utils import User, UserEdit
from ..db import client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

project_db = client.project
users_collection = project_db.get_collection("users")

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{username}", description="Get informations about an user")
async def read_user_profile(username: str = Path(..., description="Unique user name")):
    if (await users_collection.count_documents({"username": username})) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User do not exist"
        )
    else:
        user_json = await users_collection.find_one({"username": username})

        return user_json


@router.get("/{username}/posts", description="Get posts by an user")
async def read_user_posts(username: str = Path(..., description="Unique user name")):
    if (await users_collection.count_documents({"username": user.username})) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "User do not exist"


@router.get("/{username}/comments", description="Get comments by an user")
async def read_user_comments(username: str = Path(..., description="Unique user name")):
    raise NotImplementedError()


@router.post("/new", description="Create a new user")
async def create_user(user: User):
    if (await users_collection.count_documents({"username": user.username})) != 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User already exists"
        )
    else:
        user_json = jsonable_encoder(user)
        result = await users_collection.insert_one(user_json)
        print(result)
        return user_json["_id"]


@router.put("/edit", description="Edit an existing user")
async def edit_user(user: UserEdit):
    if (await users_collection.count_documents({"username": user.username})) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User do not exist"
        )
    else:
        updates = user.dict(exclude_unset=True)
        filter_row = {"username": user.username}
        result = await users_collection.update_one(filter_row, {"$set": updates})
        print(result)
        return "Updated user"


@router.put("/delete", description="Delete an existing user")
async def delete_user(user: User):
    if (await users_collection.count_documents({"username": user.username})) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User do not exist"
        )
    else:
        result = await users_collection.delete_one({"username": user.username})
        print(result)
        return "Removed user"
