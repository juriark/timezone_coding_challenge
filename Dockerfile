# syntax=docker/dockerfile:1.2

FROM python:3.10

WORKDIR /code/

# Env Vars
ENV POETRY_VERSION=1.4.0

# System deps
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Install project with dev dependencies
COPY ./pyproject.toml ./poetry.lock* /code/
RUN poetry install

COPY ./src /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]