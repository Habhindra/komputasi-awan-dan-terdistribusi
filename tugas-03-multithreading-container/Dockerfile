# TODO 1: Pilih base image Python resmi yang ringan (cari tag "slim" di Docker Hub).
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# TODO 2: Tulis perintah untuk install dependency dari requirements.txt.

COPY src/ ./src/

# TODO 3: Tulis perintah default yang dijalankan saat container start,
# yaitu menjalankan src/order_simulator.py dengan python3.
CMD ["python", "src/order_simulator_skeleton.py"]
