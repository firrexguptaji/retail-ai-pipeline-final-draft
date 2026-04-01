FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/requirements-base.txt ./requirements/
COPY requirements/requirements-gateway.txt ./requirements/

# Install dependencies
RUN pip install --no-cache-dir -r requirements/requirements-gateway.txt

# ✅ Preserve package structure
COPY common/ ./common/
COPY gateway/ ./gateway/

# Environment
ENV SERVICE_NAME=gateway

EXPOSE 5000

# ✅ Run as package
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "gateway.app:app"]