FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y python3-opencv && \
    pip install --no-cache-dir fastapi[all] pillow boto3 opencv-python-headless opencv-contrib-python

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
