#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

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
  DB_HOST=$(python -c "import os, dj_database_url; print(dj_database_url.parse(os.getenv('DATABASE_URL')).get('HOST', ''))")
  DB_PORT=$(python -c "import os, dj_database_url; print(dj_database_url.parse(os.getenv('DATABASE_URL')).get('PORT', ''))")
  DB_NAME=$(python -c "import os, dj_database_url; print(dj_database_url.parse(os.getenv('DATABASE_URL')).get('NAME', ''))")
  DB_USER=$(python -c "import os, dj_database_url; print(dj_database_url.parse(os.getenv('DATABASE_URL')).get('USER', ''))")
  DB_PASSWORD=$(python -c "import os, dj_database_url; print(dj_database_url.parse(os.getenv('DATABASE_URL')).get('PASSWORD', ''))")
fi

# Wait for the database to be ready if using external DB
if [ "$DB_TYPE" = "external" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT to be ready..."
  python - <<EOF
import psycopg2
import time
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
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
