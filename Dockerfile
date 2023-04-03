FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . /app


CMD ["adev", "runserver", "livereload", "host", "0.0.0.0", "port", "8080"]