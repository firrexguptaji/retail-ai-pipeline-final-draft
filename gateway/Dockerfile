FROM python:3.11-slim

WORKDIR /app

COPY requirements/requirements-base.txt ./requirements/
COPY requirements/requirements-gateway.txt ./requirements/

RUN pip install --no-cache-dir -r requirements/requirements-gateway.txt

COPY common/ ./common/
COPY gateway/ .

ENV SERVICE_NAME=gateway

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]