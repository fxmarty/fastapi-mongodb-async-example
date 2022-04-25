import sys
from enum import Enum
from typing import List, Optional

import pymongo
from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field
from pymongo.errors import ConnectionFailure

from .routers import comments, posts, users
from .utils import server_path

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

client = pymongo.MongoClient(server_path)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command("ismaster")
    print("Connected to MongoDB.")
except ConnectionFailure:
    print(f"Server {server} not available, exiting.")
    sys.exit(1)


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root_endpoint():
    return {"API name": "Forum API"}
