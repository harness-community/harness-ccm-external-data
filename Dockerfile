FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install --no-root

COPY src .

ENTRYPOINT [ "poetry", "--directory", "/app", "run", "python", "/app/exec.py" ]
