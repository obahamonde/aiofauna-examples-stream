FROM python:3.7.3-alpine3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["adev", "runserver", "livereload", "host", "0.0.0.0", "port", "8080"]