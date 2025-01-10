#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Kill any existing cron processes (if present)
echo "Stopping existing cron processes..."
pkill -f cron || true

# Ensure the environment is correctly configured
echo "Initializing Django environment..."
export DJANGO_SETTINGS_MODULE=beachfront_villas_padel_reservation.settings

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

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

# Set up the crontab
echo "Setting up crontab..."
crontab /etc/cron.d/cron_jobs
chmod 0644 /etc/cron.d/cron_jobs

# Start the cron service
echo "Starting cron service..."
cron

# Check if the cron service is running
echo "Checking if cron is running..."
CRON_PID=$(pgrep cron || true)

if [ -z "$CRON_PID" ]; then
    echo "Error: Cron service failed to start!"
    exit 1
else
    echo "Cron service is running with PID: $CRON_PID"
fi

# Run the default Django command (or any other command, e.g., start server)
echo "Starting the Django server..."
exec "$@"  # This will execute the command passed to the container (e.g., python manage.py runserver)
