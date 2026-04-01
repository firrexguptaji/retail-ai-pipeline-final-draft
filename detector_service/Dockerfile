FROM python:3.11-slim

WORKDIR /app

# System dependencies (needed for OpenCV + Torch)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/requirements-base.txt ./requirements/
COPY requirements/requirements-detector.txt ./requirements/

# Install dependencies
RUN pip install --no-cache-dir -r requirements/requirements-detector.txt

# Copy shared + service code
COPY common/ ./common/
COPY detector_service/ .

# Environment
ENV MODEL_PATH=/models/yolov8n.pt
ENV SERVICE_NAME=detector

EXPOSE 8001

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8001", "app:app"]