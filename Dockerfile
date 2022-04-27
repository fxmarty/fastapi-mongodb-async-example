# this dockerfile should be built as:
# `docker build -t fastapi_mongodb_example .`
# and for persistent data run as:
# `docker run --user "$(id -u):$(id -g)" -v $(pwd)/data:/data/db --net=host -it`
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN \
    wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - && \
    echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list && \
    apt-get update && \
    apt-get install -y mongodb-org && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY ./start_all.sh /code/start_all.sh

COPY ./app /code/app

CMD bash start_all.sh
