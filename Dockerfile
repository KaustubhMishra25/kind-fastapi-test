FROM python:3.11-slim

WORKDIR /fastapp

COPY ./requirements.txt /fastapp/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /fastapp/app

ENV NAME fastapi-test

CMD [ "gunicorn" , "-k", "uvicorn.workers.UvicornWorker", "-b" , "0.0.0.0:3000" , "app.main:app" ]