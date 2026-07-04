FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and self-contained synthetic dataset
COPY app ./app
COPY data ./data

# Configure environment variables
ENV DATA_DIR=/app/data/synthetic

# Start the uvicorn API server, binding dynamically to Google Cloud Run's port (default 8080)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
