FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
COPY backend/__init__.py ./backend/__init__.py
COPY backend/main.py ./backend/main.py
COPY backend/api ./backend/api
COPY backend/models ./backend/models
COPY backend/services ./backend/services
COPY backend/database ./backend/database
COPY backend/telemetry ./backend/telemetry
COPY backend/alerts ./backend/alerts

RUN pip install --no-cache-dir -r backend/requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
