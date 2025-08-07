FROM python:3.10-slim

# Install ffmpeg and other system dependencies
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV DOWNLOAD_DIR=downloads
ENV OUTPUT_DIR=clips

# Create necessary directories
RUN mkdir -p downloads clips

# Default command
CMD ["python", "main.py"]

