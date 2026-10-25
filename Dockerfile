FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend ./backend
COPY frontend ./frontend

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "backend.app", "run", "--host=0.0.0.0", "--port=5000"]