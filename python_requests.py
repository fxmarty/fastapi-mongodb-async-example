import json
from pprint import pprint
from urllib.parse import urlencode

import pydantic
import requests
from bson import ObjectId, json_util

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

session = requests.Session()


def build_url(api_url, endpoint, query):
    url = api_url + endpoint + "?" + urlencode(query)
    print(url)
    return url


api_url = "http://0.0.0.0:8000"
endpoint = "/users/new"

query = {}
method = "POST"
body = {"username": "mirai"}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

body = {"username": "sylvie"}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## create post
endpoint = "/posts/new"
query = {"username": "sylvie"}
method = "PUT"
body = {
    "title": "This is my 3 post.",
    "text": "Hello everyone I am Felix!",
    "category": "Presentations",
}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## edit post
endpoint = "/posts/edit"
post_id = "626678a7f8237a5ae82e607a"
query = {"username": "felix", "post_id": post_id}
method = "PUT"
body = {"text": "I just want to edit the text"}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## search post
endpoint = "/posts/search"
# query = {"start": "2022-01-01"}
# query = {"title": "This", "author": "sylvie"}
query = {"post_id": "6266862792fb0d6439d1530d"}
method = "GET"
body = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
res_json = response.json()
print(res_json)
res = json.loads(res_json, object_hook=json_util.object_hook)
pprint(res)
print(response.status_code)


## delete post
endpoint = "/posts/delete"
post_id = "6266649d10aa3dce9249ae8b"
query = {"username": "felix", "post_id": post_id}
method = "PUT"
body = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)


## get user details
endpoint = "/users/mirai"
query = {}
method = "GET"
body = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## edit user details
endpoint = "/users/edit"
method = "PUT"
body = {"username": "sylvie", "signature": "this is my signature2"}
query = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## edit user details
endpoint = "/users/edit"
method = "PUT"
body = {
    "username": "sylvie",
    "birthdate": "2015-06-23",
    "signature": "this is my biiis",
}
query = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## edit user details
endpoint = "/users/edit"
method = "PUT"
body = {
    "username": "sylvie",
    "birthdate": None,
    "signature": "this is my haha",
}
query = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## delete user
endpoint = "/users/delete"
method = "PUT"
body = {"username": "sylvie"}
query = {}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)

## create user
endpoint = "/users/new"
query = {}
method = "POST"
body = {"username": "felixmmm"}

response = session.request(method, url=build_url(api_url, endpoint, query), json=body)
pprint(response.json())
print(response.status_code)
