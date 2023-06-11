FROM python:3.11-slim as requirements-stage

RUN apt -qqy update

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11-slim-buster

WORKDIR /proj

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN useradd -m -d /proj -s /bin/bash app
COPY ./src /proj
RUN chown -R app:app /proj/*
USER app