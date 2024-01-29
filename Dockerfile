ARG PYTHON_VERSION=3.12-slim-bookworm

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage

RUN apt-get update && apt-get install --no-install-recommends -y build-essential

COPY requirements/local.txt .

RUN pip wheel --wheel-dir /usr/src/app/wheels -r local.txt --no-deps

FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./src/ ${APP_HOME}
