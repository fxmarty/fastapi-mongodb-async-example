import sys
from enum import Enum
from typing import List, Optional

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field

from .db import client
from .routers import comments, posts, users

tags_metadata = [
    {
        "name": "posts",
        "description": "Get informations about posts.",
    },
    {
        "name": "comments",
        "description": "Get informations about comments.",
    },
    {
        "name": "users",
        "description": "Get informations about users.",
    },
]

try:
   # The ismaster command is cheap and does not require auth.
   client.admin.command('ismaster')
   print("Connected to MongoDB server")
except Exception as e:
   print(e)


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root_endpoint():
    return {"API name": "Forum API"}
