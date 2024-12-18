# Dockerfile
FROM python:3.11.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Add crontab file
COPY crontab /etc/cron.d/reset_weekly_data

# Give execution rights to the cron job file
RUN chmod 0644 /etc/cron.d/reset_weekly_data

# Apply cron job
RUN crontab /etc/cron.d/reset_weekly_data

# Ensure cron logs are accessible
RUN touch /var/log/cron.log && chmod 666 /var/log/cron.log

# Add the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the app
CMD ["sh", "-c", "cron", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]
