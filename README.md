## Minimalist FastAPI + MongoDB example

This is a basic example on how to use FastAPI and MongoDB together, to construct a database and an API for a forum. Some parts can surely be optimized.

## How to run

This project best runs within a Docker container. Run

```
docker build -t fastapi_mongodb_example . && docker run -it --net=host fastapi_mongodb_example
```

and check both `mongod` and `unicorn` start properly. Check as well this address for Uvicorn local server (on the line `Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`).

Both MongoDB database and Unicorn server should be accessible from the host machine.

See the documentation at http://0.0.0.0:8000/redoc, and GET queries can be performed through the browser. To perform other queries, get inspiration from [python_requests](python_requests.py).

The database state can be checked with `mongosh`, e.g. with
```
mongosh
> show dbs
> use project
> db.users.find()
> db.posts.find()
```
