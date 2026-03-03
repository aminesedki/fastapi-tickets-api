# Dockerfile (repo root)
FROM python:3.12-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (adjust if you need compilation deps)
RUN apk add --no-cache bash

# install deps first (better cache)
COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

ARG INSTALL_DEV=false

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && if [ "$INSTALL_DEV" = "true" ]; then pip install --no-cache-dir -r /tmp/requirements.dev.txt; fi \
    && rm -rf /tmp/*

# copy app code
COPY ./app /app

EXPOSE 8080