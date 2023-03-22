#FROM pypy:3.9-7.3.11-buster
#
#WORKDIR /app
#COPY . /app
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN pip install --upgrade pip && \
#    pip install poetry && \
#    poetry config virtualenvs.create false && \
#    poetry poetry install --no-interaction --no-root --no-cache
#
FROM pypy:3.9-7.3.11-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ENV POETRY_HOME /opt/poetry
RUN python3 -m venv $POETRY_HOME && $POETRY_HOME/bin/pip install poetry==1.2.2
ENV POETRY_BIN $POETRY_HOME/bin/poetry
COPY pyproject.toml poetry.lock ./

RUN $POETRY_BIN config --local virtualenvs.create false && $POETRY_BIN install --no-root

COPY . /app
