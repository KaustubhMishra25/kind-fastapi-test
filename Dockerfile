FROM python:3.11-slim

WORKDIR /fastapp

COPY ./requirements.txt /fastapp/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /fastapp/app

ENV NAME fastapi-test

CMD [ "gunicorn" , "-b" , "0.0.0.0:8000" , "app.main:app" ]