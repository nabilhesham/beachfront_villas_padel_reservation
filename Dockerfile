# Dockerfile
FROM python:3.11.10-slim

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Default command to run migrations, initialize matches, and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py initialize_matches && python manage.py runserver 0.0.0.0:8000"]
