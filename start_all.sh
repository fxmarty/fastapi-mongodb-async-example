#!/bin/bash

/usr/bin/mongod &
uvicorn app.main:app --host 0.0.0.0
