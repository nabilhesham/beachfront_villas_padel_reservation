# Dockerfile
FROM python:3.11.10-slim

# Set environment variables for Django settings
#ENV DJANGO_ENV=local

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create the static files directory if it doesn't exist
RUN mkdir -p /app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Migrate DB and run scripts
RUN python manage.py migrate


# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script to run when the container starts
ENTRYPOINT ["/entrypoint.sh"]


# Default command to run migrations, initialize matches, and start the server
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
