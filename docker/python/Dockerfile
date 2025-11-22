FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Don't copy code - it will be mounted as a volume

RUN groupadd -g 1000 appgroup && \
    useradd -m -u 1000 -g appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Add --reload for auto-reload on code changes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
