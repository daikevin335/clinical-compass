# Lightweight Python app image for Clinical Compass ETL
FROM python:3.11-slim

# Avoid writing .pyc files and enable unbuffered stdout/stderr for logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required by psycopg2 binary wheel (Debian-slim)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into the image
COPY . /app

# Default command: wait for DB, then run extract -> clean -> load
CMD ["bash", "-lc", "python3 src/wait_for_db.py && python3 src/extract.py && python3 src/clean.py && python3 src/load.py"]
