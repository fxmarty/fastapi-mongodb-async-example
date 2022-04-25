FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN \
    wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - && \
    echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list && \
    apt-get update && \
    apt-get install -y mongodb-org

RUN mkdir -p /data/db

COPY ./start_all.sh /code/start_all.sh

#EXPOSE 27017
#EXPOSE 28017

#CMD ["/usr/bin/mongod"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

COPY ./app /code/app

CMD ["bash", "start_all.sh"]
