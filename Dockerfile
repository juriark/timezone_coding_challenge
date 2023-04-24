# syntax=docker/dockerfile:1.2

FROM python:3.10

WORKDIR /opt/project

# Env Vars
ENV POETRY_VERSION=1.4.0
ENV PYTHONPATH "${PYTHONPATH}:/opt/project"

# --- POETRY ---
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
# Install dependencies
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

COPY ./src ./src
COPY ./data/world ./data/world

WORKDIR /opt/project/src
#CMD ["python3", "timezones/tmp.py"]