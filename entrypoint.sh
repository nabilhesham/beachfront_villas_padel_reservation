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


# Wait for the database to be ready (if needed)
# sleep 10  # Uncomment and adjust if your DB needs time to start

# Run the create_users command to ensure users are created
echo "Creating users..."
python manage.py create_users

# Run the default Django command (or any other command)
exec "$@"