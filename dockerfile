# Lightweight Python App image for Clinical Compass ETL

FROM python:3.11-slim

# Avoid .pyc and enable unbuffered output

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /App

# system dpes for psycopg2

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \ 
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps

COPY requirements.txt ./
RUN pip install --no-chache-dor -r requirements.txt 

# Copy project code 

COPY . /app 

# Default commnad: wait for DB then run TEL sequence

CMD ["bash", "-lc", "python3 src/wait_for_db.py && python3 src/extract.py && python3 src/clean.py && python3 src/load.py"]