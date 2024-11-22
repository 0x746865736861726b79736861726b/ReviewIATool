FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc curl

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
