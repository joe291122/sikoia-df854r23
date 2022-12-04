# syntax = docker/dockerfile:1.3

ARG FUNCTION_DIR="/home/app"
ARG RUNTIME_VERSION="3.10.5"
ARG DISTRO_VERSION="3.16"

FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine

WORKDIR /code

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt --target /code/

COPY app /code/app

CMD [ "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
