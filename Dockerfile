# Dockerfile
FROM python:3.11.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=${DJANGO_ENV:-local}
ENV DATABASE_URL=${DATABASE_URL:-}

# Set the working directory
WORKDIR /app

# Install system dependencies including cron and procps (for pgrep)
RUN apt-get update && apt-get install -y cron procps

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Add the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Start the cron service and the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

