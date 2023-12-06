FROM python:3.11 as builder

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pdm.lock README.md /app/

WORKDIR /app/
RUN pdm config python.use_venv False && mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

COPY . /app/

FROM python:3.11

# retrieve packages from build stage
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.8/lib /app/pkgs

# set command/entrypoint, adapt to fit your needs
CMD ["python", "-m", "app"]