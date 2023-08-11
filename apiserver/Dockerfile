FROM python:3.11.4-slim-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "apiserver.wsgi", "-b", "0.0.0.0:8000"]