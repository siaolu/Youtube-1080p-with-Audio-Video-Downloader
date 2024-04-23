# Use an official Python runtime as a parent image
FROM python:3.9-slim as builder

# Set the working directory in the builder stage
WORKDIR /usr/src/app

# Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip, setuptools, and wheel are updated to avoid any old bugs affecting the build
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Start a new stage from a smaller base image to reduce the final image size
FROM python:3.9-slim
WORKDIR /usr/local/src/app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the application
CMD ["python", "app.py"]


# Non-root user
RUN useradd -m myuser
USER myuser

# Health check
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
