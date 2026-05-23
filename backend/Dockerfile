FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY reservas_app reservas_app
COPY alembic alembic
COPY alembic.ini ./

RUN pip install --no-cache-dir .

RUN mkdir -p /data

ENV DATABASE_URL=sqlite:////data/reservas.db

EXPOSE 8000

CMD sh -c "alembic upgrade head && uvicorn reservas_app.main:app --host 0.0.0.0 --port 8000"
