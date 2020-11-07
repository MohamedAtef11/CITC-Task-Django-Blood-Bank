FROM python:3.7-slim

USER root
RUN python -m pip install --upgrade pip

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py collectstatic


EXPOSE 8000
