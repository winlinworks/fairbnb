# Base Arguements to leverage across build stages
ARG APP_DIR=/app

#############
# Base image to use with builder and runner stages
#############
FROM python:3.12-alpine AS base
ARG APP_DIR
ARG DEV=false

ENV VIRTUAL_ENV=${APP_DIR}/.venv \
    PATH="${APP_DIR}/.venv/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

RUN apk update && \
    apk add libpq

#############
# Build (Prepare Environment) image
#############
FROM base AS build
ARG APP_DIR

# Install curl so we can get poetry
# install build-base and libffi-dev so we can install poetry and dependencies (compiles some code)
RUN apk --no-cache add curl build-base libffi-dev

# install poetry and add to path
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# change work directory for where our app will live
WORKDIR ${APP_DIR}
COPY pyproject.toml poetry.lock ./

RUN if [ $DEV ]; then \
    poetry install; \
    else \
    poetry install --only main; \
    fi


#############
# Deployment image
#############
FROM base AS run
ARG APP_DIR

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR ${APP_DIR}/
COPY  . ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
