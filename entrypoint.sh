#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Check if DJANGO_ENV is set, if not default to 'local'
DJANGO_ENV=${DJANGO_ENV:-local}
echo "DJANGO_ENV is set to: $DJANGO_ENV"
DATABASE_URL=${DATABASE_URL:-}
echo "DATABASE_URL is set to: $DATABASE_URL"

# Kill any existing cron processes (if present)
echo "Stopping existing cron processes..."
pkill -f cron || true


# Ensure the environment is correctly configured
echo "Initializing Django environment..."
export DJANGO_SETTINGS_MODULE=beachfront_villas_padel_reservation.settings

# Determine the database configuration
if [ -z "$DATABASE_URL" ]; then
  echo "Using local SQLite database for development."
  DB_TYPE="sqlite"
  DB_PATH=${DB_PATH:-/app/db.sqlite3}  # Default path to SQLite file
else
  echo "Using production database from DATABASE_URL."
  DB_TYPE="external"
  DB_URL=$DATABASE_URL  # Directly use the DATABASE_URL
fi

# Wait for the database to be ready if using external DB
if [ "$DB_TYPE" = "external" ]; then
# Wait for PostgreSQL to be ready (make sure the PostgreSQL component is running first)
echo "Waiting for database to be ready..."
python - <<EOF
import psycopg2
import time
import os

DB_URL = os.getenv("DATABASE_URL")

while True:
    try:
        # Ensure we're passing the full DATABASE_URL to psycopg2
        conn = psycopg2.connect(DB_URL)
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError as e:
        print(f"Database is not ready yet: {e}")
        time.sleep(1)
EOF
fi

# Print database tables
echo "Fetching database table names..."
python - <<EOF
import os
from django.conf import settings
from django.db import connection

if "$DB_TYPE" == "sqlite":
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.getenv("DB_PATH", "/app/db.sqlite3"),
            }
        }
    )
else:
    import dj_database_url
    settings.configure(
        DEBUG=True,
        DATABASES={"default": dj_database_url.parse(os.getenv("DATABASE_URL"))}
    )

# Initialize Django
import django
django.setup()

# Print table names
with connection.cursor() as cursor:
    tables = connection.introspection.table_names()
    print(f"Database tables: {tables}")
EOF


# Apply database migrations
echo "Applying database migrations..."
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

# Check if cron is already running
echo "Checking if cron is running..."
if ! pgrep cron > /dev/null
then
    echo "Starting cron service..."
    service cron stop
    service cron start
else
    echo "Cron service is already running."
fi

# Setup cron jobs
echo "Setting up crontab..."
(echo "0 0 * * 1 export DJANGO_ENV=$DJANGO_ENV && export DATABASE_URL=$DATABASE_URL && /usr/local/bin/python /app/manage.py reset_weekly_data >> /proc/1/fd/1 2>/proc/1/fd/2") | crontab -u root -

# Restart cron service
echo "Restarting cron service..."
service cron restart

sleep 2
# Debugging step: list the cron jobs after setting them
echo "Listing current crontab..."
crontab -l

service cron status

# Run the default Django command (or any other command, e.g., start server)
echo "Starting the Django server..."
exec "$@"  # This will execute the command passed to the container (e.g., python manage.py runserver)
