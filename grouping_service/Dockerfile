FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements-base.txt ./requirements/
COPY requirements/requirements-grouping.txt ./requirements/

RUN pip install --no-cache-dir -r requirements/requirements-grouping.txt

COPY common/ ./common/
COPY grouping_service/ .

ENV SERVICE_NAME=grouping

EXPOSE 8002

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8002", "app:app"]