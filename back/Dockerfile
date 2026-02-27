FROM python:3.13-slim
ENV PYTHONUNBUFFERED 1

# Instalar dependencias necesarias para el Dev Container y herramientas básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config gcc g++ default-libmysqlclient-dev build-essential \
    libssl-dev libffi-dev libgl1 libglib2.0-0 libgomp1 libsm6 \
    libxext6 libxrender-dev wget procps git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code
COPY pyproject.toml uv.lock* ./

# Install dependencies with uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV PATH=/code/.venv/bin:$PATH

COPY . .

EXPOSE 8000