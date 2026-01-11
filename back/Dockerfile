FROM python:3.13-slim
ENV PYTHONUNBUFFERED 1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /code
WORKDIR /code
COPY pyproject.toml /code/

# Install dependencies with uv
RUN uv sync

# Install debugpy
RUN uv pip install --system debugpy

COPY . /code/

