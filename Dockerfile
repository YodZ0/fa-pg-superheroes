# ========== Base Stage ==========
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.0.0"

RUN poetry config virtualenvs.create false

COPY poetry.lock ./
COPY pyproject.toml ./

# ========== Prod Stage ==========
FROM base AS prod

RUN poetry install --without dev

COPY . ./

RUN chmod +x prestart.sh
ENTRYPOINT ["./prestart.sh"]

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ========== Test Stage ==========
FROM base AS test

RUN poetry install

COPY . ./

RUN chmod +x prestart.sh
ENTRYPOINT ["./prestart.sh"]

CMD ["pytest", "-v"]
