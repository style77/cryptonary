FROM python:3.11 as builder

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pdm

WORKDIR /pkgs

COPY pyproject.toml pdm.lock README.md /pkgs/

RUN pdm config python.use_venv False \
    && pdm install --prod


FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

COPY --from=builder /pkgs/__pypackages__/3.11/lib /pkgs

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/pkgs

CMD ["python", "-m", "app"]