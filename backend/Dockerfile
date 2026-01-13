FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (for building psycopg2/reportlab/etc if needed)
# libpq-dev is needed for psycopg2-binary to work reliably or for compiling psycopg from source
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
