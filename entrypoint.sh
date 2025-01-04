#!/bin/bash

# Exit on errors
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Check if DJANGO_ENV is set to "production"
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Environment is production. Running production setup..."
    # Collect static files
    echo "Collecting static files..."
    mkdir -p /app/staticfiles
    python manage.py collectstatic --noinput
else
    echo "Environment is local. Skipping collectstatic..."
fi

# Run the create_users command to ensure users are created
echo "Creating users..."
python manage.py create_users

# Start cron in the background
service cron start
# Ensure cron service is running
if ! pgrep cron > /dev/null; then
    echo "Starting cron service..."
    service cron start
else
    echo "Cron is already running"
fi


# Run the default Django command (or any other command, e.g., start server)
echo "Starting the Django server..."
exec "$@"  # This will execute the command passed to the container (e.g., python manage.py runserver)
