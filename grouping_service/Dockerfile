FROM python:3.11-slim

WORKDIR /app

# System deps
# System dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Requirements
COPY requirements/requirements-base.txt ./requirements/
COPY requirements/requirements-grouping.txt ./requirements/

RUN pip install --no-cache-dir -r requirements/requirements-grouping.txt

# ✅ Preserve package structure
COPY common/ ./common/
COPY grouping_service/ ./grouping_service/

# Environment
ENV SERVICE_NAME=grouping

EXPOSE 8002

# ✅ Run as package
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8002", "grouping_service.app:app"]