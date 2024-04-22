# Stage 1: Build and compile Python dependencies
FROM python:3.9-slim as builder
WORKDIR /app

# Install packages required for compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Production environment
FROM python:3.9-slim
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /root/.local
# Copy application code
COPY . .

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and switch to it
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app_main.py"]
